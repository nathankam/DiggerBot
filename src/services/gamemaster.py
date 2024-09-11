from dataclasses import dataclass
import pytz
import random

from src.data.greetings import GREETINGS
from src.data.reacts import REACTS
from src.models.music import Theme
from src.persistence.models.contribution import Contribution
from src.persistence.models.session import Session
from src.services.helpers import get_day_indicator


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


    def start(self, theme: Theme, timezone: str) -> str:

        # Prep 
        tz = pytz.timezone(timezone)
        now = self.session.start_at.as_timezone(tz)
        vote_time = self.session.vote_at.as_timezone(tz)
        indicator = get_day_indicator(now, vote_time)
        vote_hour = vote_time.strftime('%H:%M')

        # Messages 
        snumber = f'**[SESSION {self.session.session_number}]**'
        greetings = random.choice(GREETINGS)
        theme = f"Le thème d'aujourd'hui est: **{theme.content.name.value}** \n*{theme.content.description}*"
        info = f"Vous avez jusqu'à **{self.translations[indicator]} {vote_hour}** pour proposer une track!"

        # Session Start
        return f'{snumber}\n\n {greetings} \n\n{theme} \n\n{info}'
        

    def close_participation(self, contributions: list[Contribution], streaks: dict, timezone: str) -> str: 

        # Pytz
        tz = pytz.timezone(timezone)
        now = self.session.vote_at.astimezone(tz)
        end_time = self.session.end_at.astimezone(tz)
        indicator = get_day_indicator(now, end_time)
        end_hour = end_time.strftime('%H:%M')

        info = f'Les participations sont closes! {len(contributions)} participations ont été enregistrées.'
        participants = f'\n'.join([f'**{u}** - *Contribution Streak:* **{s}**)' for u, s in streaks.items()])
        reacts_list = f'Voter avec: \n' + '\n'.join([f' {a.emoji} - *{a.meaning}*' for a in REACTS])
        vote_end = f'Vous avez jusqu\'à {self.translations[indicator]} {end_hour} pour voter!'

        return f'{info}\n\n {participants}\n\n {reacts_list}\n\n {vote_end}',
    
    
    def close_votes(self, votes: dict, winners: list) -> str: 

        info = f'Les votes sont clos! {len(votes)} votes ont été enregistrés.'
        voters = '\n'.join([f'- **{user}**  *{vote_count} votes*' for user, vote_count in votes.items() if vote_count > 0])
        
        winner_msg = f'Le gagnant d\'aujourd\'hui est: {winners[0]}'
        winners_msg = f'Les gagnants d\'aujourd\'hui sont: ' + ', '.join(winners)
        win_msg = winners_msg if len(winners) > 1 else winner_msg

        congratulations = f'Félicitations! 🎉'

        return f'{info}\n\n {voters}\n{win_msg}\n{congratulations}',

    
    @staticmethod
    def no_contributions(participation_timeout) -> str: 

        info1 = f'Aucune participation n\'a été enregistrée. 😢'
        info2 = f'Vous pouvez diminuer la fréquence des sessions en modifiant le schedule avec !set_schedule <schedule_id>. Listez la liste des schedules avec !list_schedules.'
        info3 = f"Le bot s'arrêtera d'ici {participation_timeout} session(s) si aucune participation n'est enregistrée."

        return f'{info1} \n{info2} \n{info3}'
    

    @staticmethod
    def killing_bot() -> str:

        info1 = 'Le bot s\'arrête faute de participations. 😢'
        info2 = 'Vous pouvez redémarrer le bot avec !start.'
        return f'{info1}\n{info2}'
        
