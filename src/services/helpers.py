import random
import re
from typing import Tuple

import discord
from src.data.challenges import CHALLENGES
from src.data.genres import GENRES, SUBGENRES

from src.models.badge import Badge
from src.models.music import GenreName, Theme
from src.models.settings import Settings

from src.persistence.database import DatabaseAccess
from src.persistence.models.badge import UserBadge
from src.persistence.models.contribution import Contribution
from src.persistence.models.group import Group
from src.persistence.models.session import Session
from src.persistence.models.user import User
from src.services.badger import Badger
from src.services.bot import DiscordBot
from src.services.gamemaster import GameMaster


def pick_theme(group_settings: Settings) -> Theme: 

    # Select Genre
    genre_weights = group_settings.genre_weights 
    weighted_genre_names = [genreName for genreName in GenreName for _ in range(genre_weights[genreName])]
    genreNameChoice = random.choice(weighted_genre_names)
    genre = [g for g in GENRES if genreNameChoice == g.name][0]

    # Subgenre / Genre Choice
    subgenres = [s for s in SUBGENRES if s.genre == genre]
    if random.random() < group_settings.genre_subgenre_ratio:
        genre_choice = random.choice([genre, *subgenres])
        type_choice = 'Genre' if genre_choice == genre else 'Subgenre'
    else: 
        genre_choice, type_choice = genre, 'Genre'

    # Select Challenge
    challenge = random.choice(CHALLENGES)
    if random.random() < group_settings.genre_explo_ratio:
        return Theme(type=type_choice, content=genre_choice)
    else:
        return Theme(type='Challenge', content=challenge)
    

def detect_contributions(
        messages: list[discord.Message], 
        session: Session, 
        users: list[User],
    ) -> list[Contribution]:

    # Plateforms
    plateforms = [
        {'name': 'SPOTIFY', 'search_string': '//open.spotify.com/'},
        {'name': 'YOUTUBE', 'search_string': '//www.youtube.com/watch'},
        {'name': 'SOUNDCLOUD', 'search_string': '//soundcloud.com/'},
    ]

    # Get Participations (link)
    all_matches: list[discord.Message] = []
    _plateform: list[str] = []
    _incognito: list[bool] = []

    # Active Users
    active_users = [u.discord_id for u in users if u.active and not u.frozen] 

    # Search for plateforms / Active Users / Messages
    for plateform in plateforms:
        matches = [m for m in messages if plateform['search_string'] in m.content and m.author.id in active_users]
        all_matches.extend(matches) 
        _plateform.extend([plateform['name'] for _ in range(len(matches))])
        _incognito.extend([m.guild is None for m in matches])

    # Create Participation objects
    contributions: list[Contribution] = [
        Contribution(
            message_id=m.id,
            discord_id=m.author.id,
            channel_id=session.channel_id,
            session_id=session.id,
            content=m.content,
            anonymous=_incognito[i],
            platform=_plateform[i],
            timestamp=m.created_at,
        )
        for (i, m) in enumerate(all_matches)
    ]

    # Remove duplicate participations for each user
    contributions_dict: dict[int, Contribution] = {}
    for contribution in contributions:
        user = contribution.user_discord_id
        if user not in contributions_dict:
            contributions_dict[user] = contribution
        else:
            existing_contribution = contributions_dict[user]
            if contribution.timestamp > existing_contribution.timestamp:
                contributions_dict[user] = contribution

    # Convert dictionary back to list
    contributions = list(contributions_dict.values())
    if len(contributions) > 0: print(f'[LOG] -- Unique Contributions Detected: {len(contributions)}')

    return contributions



async def vote_analysis(
        bot: DiscordBot, 
        session: Session, 
        group: Group, 
        database: DatabaseAccess,
        contributions: list[Contribution]
    ) -> Tuple[dict[int, int], list[int]]:

    # Session Channel ID
    channel_id = session.channel_id
    channel = bot.get_channel(channel_id)

    # Initialize Votes // KEYS = User Discord Id
    reacts = dict.fromkeys([c.user_discord_id for c in contributions], 0)
    vote_count = dict.fromkeys([c.user_discord_id for c in contributions], 0)
    points = dict.fromkeys([c.user_discord_id for c in contributions], 0)
    votes = dict.fromkeys([c.user_discord_id for c in contributions], [])

    # Count Votes
    for contribution in contributions: 

        # Fetch Contribution Message Reactions
        message = await channel.fetch_message(contribution.message_id)
        reactions = message.reactions

        # For each reaction, get the users who reacted: [KEY: User Id (int) / VALUE: Emoji (str)]
        contribution_reacts, contribution_emojid = {}, {}
        for reaction in reactions:

            # Fetch Users who reacted (Voters)
            reaction_users: list[discord.User] = [user async for user in reaction.users()]
            for voter in reaction_users:
                emoji_code = reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.id
                contribution_reacts[voter.id] = reaction.emoji
                contribution_emojid[voter.id] = emoji_code
                votes[voter.id].append((contribution.user_discord_id, emoji_code))

        # Count the votes
        _vote_count = len([r for u, r in contribution_emojid.items() if u != contribution.user_discord_id])
        vote_count[contribution.user_discord_id] = _vote_count
        reacts[contribution.user_discord_id] = contribution_reacts
        print(f'[LOG] -- {contribution.user_discord_id} -> {_vote_count} votes')

    # Compute Points
    vote_count = dict(sorted(vote_count.items(), key=lambda item: item[1], reverse=True))
    voters = [v for v, votes in votes.items() if len(votes) > 0]
    points, winners, banger = compute_points(points, vote_count)

    # Update Contributions and User Points 
    for contribution in contributions:
        contribution.reacts = reacts[contribution.user_discord_id]
        contribution.points = points[contribution.user_discord_id]
        if contribution.user_discord_id in winners: 
            contribution.winner = True
            contribution.banger = banger
        database.session_resource.update_contribution(contribution)

        # Points Update
        user: User = database.group_resource.get_user_by_id(contribution.user_discord_id, group.id)
        user.points = user.points + contribution.points
        database.group_resource.update_user(user)

    # Update Session
    session.voters = voters
    session.winners = winners
    session.participants = [c.user_discord_id for c in contributions]
    database.session_resource.update_session(session)

    return vote_count, winners


def compute_points(points: dict[int, int], votes: dict[int, int]) -> tuple[dict[int, int], list[int], bool]:

    # Winners definition
    winners = []
    max_votes = max(votes.values())
    for user_discord_id, vote_count in votes.items(): 
        if vote_count == max_votes: 
            winners.append(user_discord_id)
        else: 
            break 

    # Banger = 3 votes, full vote, and at least 3 votes
    is_banger = len(votes) >= 3 \
        and len(votes) == max(votes.values()) + 1 \
        and max(votes.values()) >= 3

    # Points System / 
    if len(winners) == 1:
        points[winners[0]] = 300 if is_banger else 200
    elif len(winners) > 1: 
        for w in winners: points[w] = 100

    return points, winners, is_banger



def compute_streak(user: User, session: Session) -> tuple[User, int]:

    # User Streak Update
    if user is None: 
        return None, 0

    # Streak Calculation
    if user.last_participation == session.session_number - 1 and not user.frozen:
        user.streak = user.streak + 1
    elif not user.frozen or user.last_participation != session.session_number - 1: 
        user.streak = 1
    else: pass

    # Max Streak Update
    if user.streak > user.best_streak:
        user.best_streak = user.streak

    # Last Participation Update
    user.last_participation = session.session_number

    return user, user.streak


async def kill_session(session: Session, group: Group, bot: DiscordBot, database: DatabaseAccess):

    # Participation Timeout
    last_session_number = database.session_resource.get_last_active_session_number(group.channel_id)
    participation_timeout = 3 - (session.session_number - last_session_number)
    
    if participation_timeout > 0:

        # Close Session
        database.session_resource.set_session_inactive(session)
        database.group_resource.streak_reset(group)
        await bot.send_message(
            message=GameMaster.no_contributions(session, group, participation_timeout),
            channel_id=group.channel_id
        )

    else:
        # Close Session + Kill Bot 
        group.is_active = False    
        database.session_resource.set_session_inactive(session)
        database.group_resource.update_group(group)
        await bot.send_message(
            message=GameMaster.killing_bot(group.language),
            channel_id=group.channel_id
        )


async def badge_update(users: list[User], group: Group, bot: DiscordBot, database: DatabaseAccess):

    # Badge Update
    for user in users:
        existing_userbadges: list[UserBadge] = database.group_resource.get_user_badges(user.id)
        assigned_badges: list[Badge] = Badger.assign_badges(user, database)
        existing_userbadges = [ub.id for ub in existing_userbadges]
        new_userbadges = [
            UserBadge(
                badge_name=b.name,
                badge_metal=b.metal,
                description=b.description,
                emoji=b.emoji,
                user_id=user.id, 
                group_id=group.id,
                discord_id=user.discord_id
            )
            for b in assigned_badges if f'{user.id}-{b.name}-{b.metal}' not in existing_userbadges
        ]

        # Notice badges
        database.group_resource.add_user_badges(new_userbadges)
        for m in GameMaster.badges_assigned(user, assigned_badges):
            await bot.send_message(message=m, channel_id=group.channel_id)



async def welcome_user(user: User, group: Group, bot: DiscordBot, database: DatabaseAccess):

    # Get Discord Member
    member: discord.User = bot.get_user(user.discord_id)
    
    # Register User DM Channel Id 
    dm_channel = await member.create_dm()
    user.dm_channel_id = dm_channel.id
    database.group_resource.update_user(user)

    print(f'[LOG] -- Welcoming {member.name} to the group! (DM Channel Id: {dm_channel.id})')

    # Send Welcome Message
    await dm_channel.send(GameMaster.welcome_user(group.name, user.name, group.language))
    


def extract_link(message_content: str) -> str:

    url_pattern = re.compile(r'https?://\S+')
    if url_pattern.findall(message_content):
        return url_pattern.findall(message_content)[0]
    else: 
        return None
