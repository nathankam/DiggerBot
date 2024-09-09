import datetime
import random
from typing import Union
from data.challenges import CHALLENGES
from data.commands import COMMANDS
from models.message import Command
from models.music import Genre, SubGenre, Theme

from data.reacts import REACTS
from data.genres import GENRES, SUBGENRES
from persistence.models.contribution import Contribution
from persistence.models.session import Session
from services.messenger import MessengerBot


def pick_theme(group_settings: dict = None) -> Theme: 

    # Select Genre
    weighted_genres = [genre for genre in GENRES for _ in range(genre.weight)]
    genre = random.choice(weighted_genres)

    # Extract subgenres
    subgenres = [s for s in SUBGENRES if s.genre == genre]
    genre_choice = random.choice([genre, *subgenres])

    # Select Challenge
    challenge = random.choice(CHALLENGES)

    # Decide between Genre and Challenge
    GENRE_CHALLENGE_RATIO = 0.75
    if random.random() < GENRE_CHALLENGE_RATIO:
        return Theme(
            type='Genre' if genre_choice == genre else 'SubGenre',
            content=genre_choice
        )
    else:
        return Theme(
            type='Challenge',
            content=challenge
        )
    

def detect_contributions(bot: MessengerBot, session: Session) -> list[Contribution]:

    # Plateforms
    plateforms = [
        {'name': 'SPOTIFY', 'search_string': 'spotify.com'},
        {'name': 'YOUTUBE', 'search_string': 'youtube.com'},
    ]

    # Get Participations (link)
    all_matches, pltfrm = [], []

    for plateform in plateforms:

        matches = bot.get_group_messages_within_timeframe(
            group_id=session.group_id,  
            start_time=session.start_at, 
            end_time=session.end_at,
            search_string=plateform['search_string']
        )

        all_matches.extend(matches) 
        pltfrm.extend([plateform['name'] for _ in range(len(matches))])

    # Create Participation objects
    pp_matches = [
        Contribution(
            message_id=m.message_id,
            user_id=m.sender_id,
            group_id=session.group_id,
            session_id=session.id,
            content=m.text,
            plateform=pltfrm[i],
            timestamp=m.timestamp,
        )
        for i, m in enumerate(all_matches)
    ]

    # Remove duplicate participations for each user
    contributions_dict = {}
    for contribution in pp_matches:
        user = contribution.user_id
        if user not in contributions_dict:
            contributions_dict[user] = contribution
        else:
            existing_participation = contributions_dict[user]
            if contribution.timestamp > existing_participation.timestamp:
                contributions_dict[user] = contribution

    # Convert dictionary back to list
    participations = list(contributions_dict.values())

    return participations



def count_votes(bot: MessengerBot, session: Session, contributions: list[Contribution]):

    # Session Group ID
    group_id = session.group_id

    # Initialize Votes
    reacts = dict.fromkeys([c.user_id for c in contributions], 0)
    votes = dict.fromkeys([c.user_id for c in contributions], 0)
    points = dict.fromkeys([c.user_id for c in contributions], 0)

    # Count Votes
    for contribution in contributions: 
        
        react_dict = bot.get_message_reacts(
            message_id = contribution.message_id, 
            group_id = group_id
        )

        translation = {a.emoji: a.name for a in REACTS}

        # Translate the reacts // Exclude the user's own reaction
        react_dict_translated = {u: translation[r] for u, r in react_dict.items() if u != contribution.user_id}

        # Count the votes
        vote_count = len([r for r in react_dict_translated.values() if r in ['VOTE', 'COUPDECOEUR']])

        votes[contribution.user_id] = vote_count
        reacts[contribution.user_id] = react_dict

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
    if len(winners >= 3):
        for w in winners: 
            points[w] = 1

    for winner in winners: 
        points[winner] = 1

    return votes, reacts, winners, points, is_banger



def get_session_number() -> int: 

    return 1


def get_day_indicator(datetime_now: datetime.datetime, datetime_next: datetime.datetime) -> str: 

    if datetime_now.day == datetime_next.day:
        return 'today'
    elif datetime_next.day - datetime_now.day == 1:
        return 'tomorrow'
    else:
        return datetime_next.strftime("%A").lower()
