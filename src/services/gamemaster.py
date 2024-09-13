from dataclasses import dataclass
from typing import Optional
import pytz
import random

from src.data.greetings import GREETINGS
from src.data.reacts import REACTS
from src.models.music import Theme
from src.persistence.models.contribution import Contribution
from src.persistence.models.group import Group
from src.persistence.models.session import Session


TRANSLATIONS = {
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


class GameMaster: 

    @staticmethod
    def start(theme: Theme, group: Group, session: Session) -> str:

        # Prep 
        tz = pytz.timezone(group.timezone)
        now = session.start_at.astimezone(tz)
        vote_time = session.vote_at.astimezone(tz)
        indicator = GameMaster.get_day_indicator(now, vote_time)
        vote_hour = vote_time.strftime('%H:%M')

        # Message
        m = f'**[SESSION {session.session_number}]**' + \
            f'\n\n{random.choice(GREETINGS)}' + \
            f'\n\nLe thème d\'aujourd\'hui est: **{theme.content.name.value}** \n*{theme.content.description}*' + \
            f'\n\nVous avez jusqu\'à **{TRANSLATIONS[indicator]} {vote_hour}** pour proposer une track!'

        # Session Start
        return m
    
        
    @staticmethod
    def close_participation(session: Session, contributions: list[Contribution], streaks: dict, timezone: str) -> str: 

        # Pytz
        tz = pytz.timezone(timezone)
        now = session.vote_at.astimezone(tz)
        end_time = session.end_at.astimezone(tz)
        indicator = GameMaster.get_day_indicator(now, end_time)
        end_hour = end_time.strftime('%H:%M')

        m = f'Les participations sont closes! {len(contributions)} participations ont été enregistrées.\n\n' + \
            f'\n'.join([f'**{u}** - *Contribution Streak:* **{s}**)' for u, s in streaks.items()]) + \
            f'\n\nVotez avec: \n' + '\n'.join([f' {a.emoji} - *{a.meaning}*' for a in REACTS]) + \
            f'\n\nVous avez jusqu\'à {TRANSLATIONS[indicator]} {end_hour} pour voter!'
        
        mi = f'Les participations sont closes! {len(contributions)} participations ont été enregistrées.\n\n' + \
            f'\n\nVotez avec: \n' + '\n'.join([f' {a.emoji} - *{a.meaning}*' for a in REACTS]) + \
            f'\n\nVous avez jusqu\'à {TRANSLATIONS[indicator]} {end_hour} pour voter!'
        
        return mi if session.incognito else m
    
    
    @staticmethod
    def anonymous_contributions(contributions: list[Contribution]) -> Optional[list[str]]:

        anonymous_contrib = [c for c in contributions if c.anonymous]
        if len(anonymous_contrib) == 0: return None

        messages = [f'Il y a eu {len(anonymous_contrib)} anonymes!']
        for c in anonymous_contrib:
            messages.append(f'🥸 Anonymous contribution: {c.content}')

        return messages
    

    @staticmethod
    def close_votes(votes: dict, winners: list) -> str: 

        voters = '\n'.join([f'- **{user}**  *{vote_count} votes*' for user, vote_count in votes.items() if vote_count > 0])
        winner_msg = f'Le gagnant d\'aujourd\'hui est: {winners[0]}'
        winners_msg = f'Les gagnants d\'aujourd\'hui sont: ' + ', '.join(winners)
        win_msg = winners_msg if len(winners) > 1 else winner_msg

        m = f'Les votes sont clos! {len(votes)} votes ont été enregistrés.' + \
            f'\n\n{voters}' + \
            F'\n{win_msg}' + \
            f'Félicitations! 🎉'
    

    @staticmethod
    def welcome(): 

        m = f'\n**Bienvenue!** 🎶' + \
            f'\n\n- Je suis DiggerBot, passioné de musique, je suis toujours à la recherche de nouveaux son! ' + \
            f'L\'objectif de ce groupe c\'est de collaborer pour découvrir de nouvelles choses. ' + \
            f'\n- A chaque session, je propose un thème et les membres du groupe sont libres de participer en partagant un lien Spotify, Youtube ou Soundcloud. ' + \
            f'A la fin du temps imparti, tout le monde peut réagir aux contributions des autres avec des reacts qui correspondent à différent types de vote.' + \
            f'Les musiques les plus votées rapportent des points pour encourager les plus fins explorateurs et un système de streak/badges récompense les participants les plus assidus.' + \
            f'Tout les mois, je publie des statistiques sur les sessions, crée une playlist spotify avec les meilleurs musiques du mois et descerne le *Digger-of-the-Month* Award.' + \
            f'\n- Comme chaque groupe est unique, vous pouvez personnaliser mes paramètres pour que je m\'adapte à vos préférences.' + \
            f'Vous pouvez par exemple changer la fréquence à laquelle je lance les sessions en selectionnant un *schedule*, ' + \
            f'ou encore changer la fréquence à laquelle chaque genre musical est proposé...' + \
            f'\n\nPour commencer, tape !me <username> pour créer un profil à ton nom.' + \
            f'\n\n*Taper !help pour plus d\'infos sur comment interragir avec mes paramètres.*\n'

        return m
    

    @staticmethod
    def welcome_user(group_name: str, user_name: str) -> str:

        m = f'Hello **{user_name}**!' + \
            f'\n\nTu as été ajouté au groupe {group_name}! Je te fais un petit rappel sur le fonctionnement du bot!' + \
            f'\n\n- A chaque session, je propose un thème et les membres du groupe sont libres de participer en partagant un lien Spotify, Youtube ou Soundcloud.' + \
            f'A la fin du temps imparti pour les contributions, tout le monde peut réagir aux liens partagés par les autres avec des reacts qui correspondent à différent types de vote.' + \
            f'Les musiques les plus votées rapportent des points pour encourager les plus fins explorateurs et un système de streak/badges récompense les participants les plus assidus.' + \
            f'Tout les mois, je publie des statistiques sur les sessions, crée une playlist spotify avec les meilleurs musiques du mois et descerne le *Digger-of-the-Month Award*.' + \
            f'Un peu comme un club de lecture, mais pour découvrir des artistes et des sons!' + \
            f'\n- Comme chaque groupe est unique, vous pouvez personnaliser mes paramètres pour que je m\'adapte à vos préférences.' + \
            f'Vous pouvez par exemple changer la fréquence à laquelle je lance les sessions en selectionnant un *schedule*, ' + \
            f'ou encore changer la fréquence à laquelle chaque genre musical est proposé...' + \
            f'\n\nJe ne communique que dans le canal general, mais si le groupe passe en mode incognito, tu pourras partager ta contribution en privé ici et je la transmettrai dans le canal général pour qu\'elle reste anonyme' + \
            f'Voila, tu sais tout! Hate d\'écouter ce que tu vas partager! 🎷\n'
        
        return m
    

    @staticmethod
    def get_day_indicator(datetime_now, datetime_next): 

        if datetime_now.day == datetime_next.day:
            return 'today'
        elif datetime_next.day - datetime_now.day == 1:
            return 'tomorrow'
        else:
            return datetime_next.strftime("%A").lower()

    
    @staticmethod
    def incognito_on() -> str: 

        m = f'*Le groupe est passé en mode incognito!*' + \
            f'\nÀ partir de maintenant, partage tes liens ici et je les transmettrai dans le groupe pour que ta contribution reste anonyme. 🥸\n'

        return m

    @staticmethod
    def incognito_off() -> str: 

        m = f'*Le groupe n\'est plus en mode incognito!*' + \
            f'\nÀ partir de maintenant, partage tes liens directement dans le canal général. 🎶\n'

        return m

    
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
        
