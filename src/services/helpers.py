import random
from typing import Tuple

import discord
from src.data.challenges import CHALLENGES
from src.data.genres import GENRES, SUBGENRES

from src.models.music import GenreName, Theme
from src.models.settings import Settings

from src.persistence.database import DatabaseAccess
from src.persistence.models.contribution import Contribution
from src.persistence.models.group import Group
from src.persistence.models.session import Session
from src.persistence.models.user import User
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
            user_id=m.author.id,
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
        user = contribution.user_id
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



async def count_votes(
        bot: DiscordBot, 
        session: Session, 
        contributions: list[Contribution]
        ) -> Tuple[dict[int, int], dict[int, dict[int, str]], list[int], dict[int, int], bool]:

    # Session Channel ID
    channel_id = session.channel_id
    channel = bot.get_channel(channel_id)

    # Initialize Votes // KEYS = User Discord Id
    reacts = dict.fromkeys([c.user_id for c in contributions], 0)
    votes = dict.fromkeys([c.user_id for c in contributions], 0)
    points = dict.fromkeys([c.user_id for c in contributions], 0)

    # Count Votes
    for contribution in contributions: 

        message = await channel.fetch_message(contribution.message_id)
        reactions = message.reactions

        # Get User Reacts for contribution: KEY: User Id (int) / 
        user_reacts, user_emojid = {}, {}
        for reaction in reactions:
            reaction_users: list[discord.User] = [user async for user in reaction.users()]
            for user in reaction_users:
                emoji_code = reaction.emoji if isinstance(reaction.emoji, str) else reaction.emoji.id
                user_reacts[user.id] = reaction.emoji
                user_emojid[user.id] = emoji_code

        print('[LOG] -- User Reacts:', user_reacts)
        print('[LOG] -- User Emoji Ids:', user_emojid)

        # Count the votes
        vote_count = len([r for r in user_emojid.values() if r in ['VOTE', 'COUPDECOEUR']])
        print(f'[LOG] -- {contribution.user_id} - {vote_count} votes')

        votes[contribution.user_id] = vote_count
        reacts[contribution.user_id] = user_reacts


    # Sort Votes 
    votes = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))

    # Compute Points
    points, winners, banger = compute_points(points, votes)

    return votes, reacts, winners, points, banger


def compute_points(points: dict[int, int], votes: dict[int, int]) -> tuple[dict[int, int], list[int], bool]:

    # Winners definition
    winners = []
    max_votes = max(votes.values())
    for user_id, vote_count in votes.items(): 
        if vote_count == max_votes: 
            winners.append(user_id)
        else: 
            break 

    # Banger = 3 votes, full vote, and at least 3 votes
    is_banger = len(votes) >= 3 \
        and len(votes) == max(votes.values()) + 1 \
        and max(votes.values()) >= 3

    # Points System / 
    if len(winners) == 1:
        points[winners[0]] = 3 if is_banger else 2
    elif len(winners) > 1: 
        for w in winners: points[w] = 1

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
    



