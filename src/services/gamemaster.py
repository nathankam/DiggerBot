from dataclasses import dataclass
import datetime
import random
from typing import Union

from src.data.greetings import GREETINGS
from src.data.reacts import REACTS
from src.models.message import TextMessage
from src.models.music import Challenge, Genre, SubGenre, Theme
from src.models.participation import Participation
from src.persistence.models.contribution import Contribution
from src.persistence.models.session import Session
from src.services.discord import DiscordBot
from src.services.helpers import get_day_indicator
from src.services.messenger import MessengerBot 


def get_user_streak(user: str) -> int: 
    return 0

class GameMaster: 

    def __init__(self, session: Session): 
        
        self.session: Session = session

        self.translations = {
            'tomorrow': 'demain',
            'today': 'aujourd\'hui',
            'monday': 'lundi',
            'tuesday': 'mardi',
            'wednesday': 'mercredi',
            'thursday': 'jeudi',
            'friday': 'vendredi',
            'saturday': 'samedi',
            'sunday': 'dimanche',
        }
            

    def start(self, theme: Theme) -> str:

        # Prep 
        now = self.session.start_at
        vote_time = self.session.vote_at
        indicator = get_day_indicator(now, vote_time)
        vote_hour = vote_time.strftime('%H:%M')

        # Messages 
        snumber = f'[SESSION {self.session.session_number}]'
        greetings = random.choice(GREETINGS)
        theme = f"Le thème d'aujourd'hui est: \n{self.theme.content.name} -- {self.theme.content.description}"
        info = f"Vous avez jusqu'à {self.translations(indicator)} {vote_hour} pour proposer une track!"

        # Session Start
        return f'{snumber}\n\n {greetings} \n\n{theme} \n{info}'
        
    

    def close_participation(self, contributions: list[Contribution], streaks: dict) -> str: 

        # Vote end
        now = self.session.vote_at
        end_time = self.session.end_at
        indicator = get_day_indicator(now, end_time)
        end_hour = end_time.strftime('%H:%M')

        info = f'Les participations sont closes! {len(contributions)} participations ont été enregistrées.'
        participants = '\n'.join([f'➡️ {u} - (contribution streak: {s})' for u, s in streaks.items])
        reacts_list = 'Voter avec: \n' + '\n'.join([f'{a.emoji} - {a.meaning}' for a in REACTS])
        vote_end = f'Vous avez jusqu\'à {self.translations(indicator)} {end_hour} pour voter!'

        return f'{info} \n{participants} \n{reacts_list} \n{vote_end}',
    
    
    def close_votes(self, votes: dict, winners: list) -> str: 

        info = f'Les votes sont clos! {len(votes)} votes ont été enregistrés.'
        voters = '\n'.join([f'➡️ {user} - {vote_count} votes' for user, vote_count in votes.items() if vote_count > 0])
        
        winner_msg = f"Le gagnant d'aujourd'hui est: {winners[0]}" 
        winners_msg = "Les gagnants d'aujourd'hui sont: " + ', '.join(winners)
        win_msg = winners_msg if len(winners) > 1 else winner_msg

        congratulations = 'Félicitations! 🎉'

        return f'{info} \n{voters} \n{win_msg} \n{congratulations}',

    
    @staticmethod
    def no_contributions(participation_timeout) -> str: 

        info1 = 'Aucune participation n\'a été enregistrée. 😢'
        info2 = 'Vous pouvez diminuer la fréquence des sessions en modifiant le schedule avec !set_schedule <schedule_id>. Listez la liste des schedules avec !list_schedules.'
        info3 = f"Le bot s'arrêtera d'ici {participation_timeout} session(s) si aucune participation n'est enregistrée."

        return f'{info1} \n{info2} \n{info3}'
    

    @staticmethod
    def killing_bot() -> str:

        info1 = 'Le bot s\'arrête faute de participations. 😢'
        info2 = 'Vous pouvez redémarrer le bot avec !start.'
        return f'{info1} \n{info2}'
        
    


    













class GameMaster2: 

    def __init__(
            self, 
            bot: MessengerBot, 
            theme: Union[Genre, SubGenre, Challenge], 
            group_id: int
        ):

        self.bot = bot
        self.theme = theme
        self.group_id = group_id
        self.session_number = 888

        self.participations = []
        self.votes = {}
        self.winners = []

        self.start_time = None
        self.vote_time = None
        self.end_time = None


    def start(self): 

        # Prep
        self.start_time = datetime.now(datetime.timezone(datetime.timedelta(hours=1)))
        self.vote_time = self.start_time + datetime.timedelta(seconds=PP_TIMEOUT_S)
        self.end_time = self.vote_time + datetime.timedelta(seconds=VOTE_TIMEOUT_S)

        # Messages 
        snumber = f'[SESSION {self.session_number}]'
        greetings = random.choice(GREETINGS)
        theme = f"Le thème d'aujourd'hui est: \n {self.theme.name} -- {self.theme.descripion}"
        info = f"Vous avez jusqu'à {self.vote_time.strftime('%H:%M')} pour proposer une track!"

        # Session Start
        return TextMessage(
            text=f'{snumber}\n\n {greetings} \n\n{theme} \n{info}'
        )


    def close_participations(self) -> TextMessage: 

        # Get Participations
        self.participations = self.detect_participations()

        # Get User Dict 
        user_dict = {p.user: p.user for p in self.participations}

        info = f'Les participations sont closes! {len(self.participations)} participations ont été enregistrées.'
        participants = '\n'.join([f'➡️ {user_dict[p.user]} - (streak: {get_user_streak(p.user)})' for p in self.participations])
        reacts_list = 'Voter avec: \n' + '\n'.join([f'{a.emoji} - {a.meaning}' for a in REACTS])
        vote_end = f'Vous avez jusqu\'à {self.end_time.strftime("%H:%M")} pour voter!'

        return TextMessage(
            text=f'{info} \n{participants} \n{reacts_list} \n{vote_end}',
        )


    def close_votes(self) -> TextMessage: 

        self.votes = self.count_votes(self.participations)
        winners = GameMaster.get_winners(self.votes)

        info = f'Les votes sont clos! {len(self.votes)} votes ont été enregistrés.'
        voters = '\n'.join([f'➡️ {user} - {vote_count} votes' for user, vote_count in self.votes.items() if vote_count > 0])
        
        winner_msg = f"Le gagnant d'aujourd'hui est: {winners[0]}" 
        winners_msg = "Les gagnants d'aujourd'hui sont: " + ', '.join(winners)

        win_msg = winners_msg if len(winners) > 1 else winner_msg

        congratulations = 'Félicitations! 🎉'

        return TextMessage(
            text=f'{info} \n{voters} \n{win_msg} \n{congratulations}',
        )

    def detect_participations(self) -> list[Participation]:
        
        # Plateforms
        plateforms = [
            {'name': 'SPOTIFY', 'search_string': 'spotify.com'},
            {'name': 'YOUTUBE', 'search_string': 'youtube.com'},
        ]

        # Get Participations (link)
        all_matches, pltfrm = [], []
        for plateform in plateforms:

            matches = self.bot.get_group_messages_within_timeframe(
                group_id=self.group_id,  
                start_time=self.start_time, 
                end_time=self.vote_time,
                search_string=plateform['search_string']
            )

            all_matches.extend(matches) 
            pltfrm.extend([plateform['name'] for _ in range(len(matches))])

        # Create Participation objects
        pp_matches = [
            Participation(
                id=m.message_id,
                user=m.sender_id,
                timestamp=m.timestamp,
                plateform=pltfrm[i],
                link=m.text, 
            ) for i, m in enumerate(all_matches)
        ]

        # Remove duplicate participations for each user
        participations_dict = {}
        for participation in pp_matches:
            user = participation.user
            if user not in participations_dict:
                participations_dict[user] = participation
            else:
                existing_participation = participations_dict[user]
                if participation.timestamp > existing_participation.timestamp:
                    participations_dict[user] = participation

        # Convert dictionary back to list
        participations = list(participations_dict.values())

        return participations
    

    def count_votes(self, participations: list[Participation]) -> dict:
    
        votes = dict.fromkeys([p.user for p in participations], 0)
        for p in participations:
            # In the USERID: REACT key pair dict
            react_dict = self.bot.get_message_reacts(p.id, self.group_id)
            translation = {a.emoji: a.name for a in REACTS} # EMOJI CODE --> ACTION NAME
            react_dict_translated = {u: translation[r] for u, r in react_dict.items()}  # USER --> ACTION NAME
            vote_count = len([r for r in react_dict_translated.values() if r in ['VOTE', 'COUPDECOEUR']])
            votes[p.user] = vote_count

        # Sort Votes 
        votes = dict(sorted(votes.items(), key=lambda item: item[1], reverse=True))

        return votes
    

    @classmethod
    def get_winners(votes: dict) -> list[str]: 

        winners = []
        max_votes = max(votes.values())
        for user, vote_count in votes.items(): 
            if vote_count == max_votes: 
                winners.append(user)
            else: 
                break 

        return winners
    





    


    


    




