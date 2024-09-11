import asyncio
import datetime
import random

import discord
from src.data.challenges import CHALLENGES
from src.data.genres import GENRES, SUBGENRES

from src.models.music import GenreName, Theme
from src.models.settings import Settings

from src.persistence.models.contribution import Contribution
from src.persistence.models.session import Session
from src.persistence.models.user import User
from src.services.bot import DiscordBot


def pick_theme(group_settings: Settings) -> Theme: 

    # Select Genre
    genre_weights = group_settings.genre_weights 
    weighted_genre_names = [genreName for genreName in GenreName for _ in range(genre_weights[genreName])]
    genreNameChoice = random.choice(weighted_genre_names)
    genre = [g for g in GENRES if genreNameChoice == g.name][0]

    # Subgenre / Genre Choice
    subgenres = [s for s in SUBGENRES if s.genre == genre]
    if random.random() < group_settings.genre_subgenre_ratio:
        genre_choice, type_choice = random.choice(subgenres), 'SubGenre'
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
        users: list[User]
    ) -> list[Contribution]:

    # Plateforms
    plateforms = [
        {'name': 'SPOTIFY', 'search_string': '//open.spotify.com/'},
        {'name': 'YOUTUBE', 'search_string': '//www.youtube.com/watch'},
    ]

    # Get Participations (link)
    all_matches: list[discord.Message] = []
    pltfrm: list[str] = []

    # Active Users
    active_users = [u.discord_id for u in users if u.active and not u.frozen] 

    # Search for plateforms / Active Users / Messages
    for plateform in plateforms:
        matches = [m for m in messages if plateform['search_string'] in m.content]
        matches = [m for m in matches if m.author.id in active_users]
        all_matches.extend(matches) 
        pltfrm.extend([plateform['name'] for _ in range(len(matches))])

    # Create Participation objects
    contributions: list[Contribution] = [
        Contribution(
            message_id=m.id,
            user_id=m.author.id,
            channel_id=session.channel_id,
            session_id=session.id,
            content=m.content,
            platform=pltfrm[i],
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
    participations = list(contributions_dict.values())
    print(f'[LOG] -- Unique Contributions Detected: {len(participations)}')

    return participations



async def count_votes(bot: DiscordBot, session: Session, contributions: list[Contribution]):

    # Session Channel ID
    channel_id = session.channel_id
    channel = bot.get_channel(channel_id)

    # Initialize Votes
    reacts = dict.fromkeys([c.user_id for c in contributions], 0)
    votes = dict.fromkeys([c.user_id for c in contributions], 0)
    points = dict.fromkeys([c.user_id for c in contributions], 0)

    # Count Votes
    for contribution in contributions: 

        message = await channel.fetch_message(contribution.message_id)
        reactions = message.reactions

        user_reacts, user_emojid = {}, {}
        for reaction in reactions:
            reaction_users = [user async for user in reaction.users()]
            for user in reaction_users:
                user_reacts[user.id] = reaction.emoji
                user_emojid[user.id] = reaction.emoji.id


        # Translate the reacts // Exclude the user's own reaction
        # emoji_translation = {a.emoji: a.name for a in REACTS}
        # react_dict_translated = {u: emoji_translation[r] for u, r in user_reacts.items() if u != contribution.user_id}

        # Count the votes
        vote_count = len([r for r in user_emojid.values() if r in ['VOTE', 'COUPDECOEUR']])

        votes[contribution.user_id] = vote_count
        reacts[contribution.user_id] = user_reacts


    # Sort Votes 
    votes = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))

    # Winner
    winners = []
    max_votes = max(votes.values())
    for user, vote_count in votes.items(): 
        if vote_count == max_votes: 
            winners.append(user)
        else: 
            break 

    # Banger 
    is_banger = len(votes) >= 3 and sum(votes.values()) - 1 == max(votes.values()) and max(votes.values()) >= 3

    if is_banger:
        points[winner] = 5 

    if len(winners) == 1:
        points[winners[0]] = 3
    if len(winners) == 2: 
        points[winners[0]] = 2
        points[winners[1]] = 2
    if len(winners) >= 3:
        for w in winners: 
            points[w] = 1

    for winner in winners: 
        points[winner] = 1

    return votes, reacts, winners, points, is_banger


def get_day_indicator(datetime_now: datetime.datetime, datetime_next: datetime.datetime) -> str: 

    if datetime_now.day == datetime_next.day:
        return 'today'
    elif datetime_next.day - datetime_now.day == 1:
        return 'tomorrow'
    else:
        return datetime_next.strftime("%A").lower()
