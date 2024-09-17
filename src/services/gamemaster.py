from dataclasses import dataclass
from typing import Optional
import pytz
import random

from src.data.greetings import GREETINGS, BRAVO
from src.data.reacts import REACTS
from src.models.music import Theme
from src.persistence.models.contribution import Contribution
from src.persistence.models.group import Group
from src.persistence.models.session import Session
from src.persistence.models.user import User


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

        # Theme
        if theme.type == 'Genre':
            theme_name = f'**{theme.content.name.value}**'
        elif theme.type == 'SubGenre':
            theme_name = f'**{theme.content.name}** -- (Subgenre of ***{theme.content.genre.name.value}***)'
        else:
            theme_name = f'{theme.content.name}'

        # Message
        m = f'**[SESSION {session.session_number} / START]**' + \
            f'\n\n{random.choice(GREETINGS)}' + \
            f'\n\nLe thème d\'aujourd\'hui est: **{theme_name}** \n*{theme.content.description}*' + \
            f'\n\nVous avez jusqu\'à **{TRANSLATIONS[indicator]} {vote_hour}** pour proposer une track!'

        # Session Start
        return m
    

    @staticmethod   
    def start_dm(theme: Theme, group: Group, session: Session) -> str:

        # Prep 
        tz = pytz.timezone(group.timezone)
        now = session.start_at.astimezone(tz)
        vote_time = session.vote_at.astimezone(tz)
        indicator = GameMaster.get_day_indicator(now, vote_time)
        vote_hour = vote_time.strftime('%H:%M')

        # Theme
        if theme.type == 'Genre':
            theme_name = f'**{theme.content.name.value}**'
        elif theme.type == 'SubGenre':
            theme_name = f'**{theme.content.name}** -- (Subgenre of ***{theme.content.genre.name.value}***)'
        else:
            theme_name = f'{theme.content.name}'

        m = f'**[SESSION {session.session_number} (***G{group.id}***) / START]**' + \
            f'\n\nLa session est en mode incognito 🥸.' + \
            f'\nTu peux partager ton lien ici, **en répondant à ce message** ↩, et je m\'occupe du reste!' + \
            f'\n\nThème: {theme_name} \n*{theme.content.description}*' + \
            f'\n\nTu as jusqu\'à **{TRANSLATIONS[indicator]} {vote_hour}** pour proposer une track!'
        
        return m
    
        
    @staticmethod
    def close_participation(session: Session, contributions: list[Contribution], streaks: dict, timezone: str) -> str: 

        # Pytz
        tz = pytz.timezone(timezone)
        now = session.vote_at.astimezone(tz)
        end_time = session.end_at.astimezone(tz)
        indicator = GameMaster.get_day_indicator(now, end_time)
        end_hour = end_time.strftime('%H:%M')

        # Variable discourse
        cont = f'participation a été enregistrée.' if len(contributions) == 1 else f'participations ont été enregistrées.'
        users = f'\n\n' + f'\n'.join([f'{GameMaster.space_padding(u, 20)} - *Streak:* ***{s}***' for u, s in streaks.items()])

        m = f'**[SESSION {session.session_number} / VOTE]**' + \
            f'\n\nLes participations sont closes! {len(contributions)} {cont}' + \
            (users if not session.incognito else '') + \
            f'\n\nVotez avec: \n' + '\n'.join([f' {a.emoji} - *{a.meaning}*' for a in REACTS]) + \
            f'\n\nVous avez jusqu\'à {TRANSLATIONS[indicator]} {end_hour} pour voter!'
        
        return m
    

    @staticmethod
    def anonymous_contributions(anonymous_contributions: list[Contribution]) -> Optional[list[str]]:

        messages = []
        for c in anonymous_contributions:
            messages.append(f'🥸 [ANONYMOUS CONTRIBUTION] -- {c.content}')

        return messages
    

    @staticmethod
    def close_votes(session: Session, users: list[User], votes: dict, winners: list) -> str: 

        # Winners translation
        winners_dict = {u.discord_id: u.name for u in users}
        winners_names = [winners_dict.get(w, 'unknown') for w in winners]

        # Votes 
        vote = 'vote a été enregistré.' if len(votes) == 1 else 'votes ont été enregistrés.'

        voters = '\n'.join([f'- **{user}**  *{vote_count} votes*' for user, vote_count in votes.items() if vote_count > 0])
        winner_msg = f'Le gagnant d\'aujourd\'hui est: *{winners_names[0]}*'
        winners_msg = f'Les gagnants d\'aujourd\'hui sont: ' + ', '.join(winners_names)
        win_msg = winners_msg if len(winners) > 1 else winner_msg

        m = f'**[SESSION {session.session_number} / RESULTS]**' + \
            f'\n\nLes votes sont clos! {len(votes)} {vote}' + \
            f'\n\n{voters}' + \
            F'\n{win_msg}' + \
            f'\n\n{random.choice(BRAVO)}'
        
        return m
    

    @staticmethod
    def welcome(): 

        m = f'\n**Bienvenue!** 🎶' + \
            f'\n- Je suis DiggerBot, passioné de musique, je suis toujours à la recherche de nouveaux son! ' + \
            f'L\'objectif de ce groupe c\'est de collaborer pour découvrir de nouvelles pépites. ' + \
            f'\n- A chaque session, je propose un thème et les membres du groupe sont libres de participer en partagant un lien Spotify, Youtube ou Soundcloud. ' + \
            f'A la fin du temps imparti, tout le monde peut réagir aux contributions des autres avec des reacts qui correspondent à différent types de vote. ' + \
            f'\n- Les musiques les plus votées rapportent des points pour encourager les plus fins explorateurs et un système de streak/badges récompense les participants les plus assidus.' + \
            f'Tout les mois, je publie des statistiques sur les sessions, crée une playlist spotify avec les meilleurs musiques du mois et descerne le *Digger-of-the-Month* Award.' + \
            f'\n- Comme chaque groupe est unique, vous pouvez personnaliser mes paramètres pour que je m\'adapte à vos préférences.' + \
            f'Vous pouvez par exemple changer la fréquence à laquelle je lance les sessions en selectionnant un *schedule*, ' + \
            f'ou encore changer la fréquence à laquelle chaque genre musical est proposé...' + \
            f'\n\nPour commencer, tape `!me <username>` pour créer un profil à ton nom.' + \
            f'\n\n* `!help` pour plus d\'infos sur comment interragir avec mes paramètres.*\n'

        return m
    

    @staticmethod
    def welcome_user(group_name: str, user_name: str) -> str:

        m = f'Hello **{user_name}**!' + \
            f'\nTu as été ajouté(e) au groupe ***{group_name}***! Je te fais un petit rappel sur le fonctionnement du groupe: ' + \
            f'\n- A chaque session, je propose un thème et les membres du groupe sont libres de participer en partagant un lien Spotify, Youtube ou Soundcloud. ' + \
            f'A la fin du temps imparti pour les contributions, tout le monde peut réagir aux liens partagés par les autres avec des reacts qui correspondent à différent types de vote. ' + \
            f'Les musiques les plus votées rapportent des points pour encourager les plus fins explorateurs et un système de streak/badges récompense les participants les plus assidus. ' + \
            f'Tout les mois, je publie des statistiques sur les sessions, crée une playlist spotify avec les meilleurs musiques du mois et descerne le *Digger-of-the-Month Award*.' + \
            f'\n- Comme chaque groupe est unique, vous pouvez personnaliser mes paramètres pour que je m\'adapte à vos préférences. ' + \
            f'Vous pouvez par exemple changer la fréquence à laquelle je lance les sessions en selectionnant un *schedule*, ' + \
            f'ou encore changer la fréquence à laquelle chaque genre musical est proposé...' + \
            f'\n- Je ne communique que dans le canal general, mais si le groupe passe en mode incognito, tu pourras partager ta contribution en privé ici et je la transmettrai dans le canal général pour qu\'elle reste anonyme' + \
            f'\n\nVoila, tu sais tout! Hate d\'écouter ce que tu vas partager! 🎷\n'
        
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
    def no_contributions(session: Session, participation_timeout) -> str: 

        m = f'**[SESSION {session.session_number} / END]**' + \
            f'\n\nAucune participation n\'a été enregistrée. ' + \
            f'Vous pouvez diminuer la fréquence des sessions en modifiant le schedule avec `!schedule_set <schedule_id>`. Listez la liste des schedules avec `!schedule_list`.' + \
            f"\n\n*Le bot s'arrêtera d'ici {participation_timeout} session(s) si aucune participation n'est enregistrée.*"

        return m
    

    @staticmethod
    def not_enough_users(users: list[User], min_users: int) -> str: 

        pp = ', '.join([u.name for u in users])
        participants = f'(Aucun utilisateur enregistré.)' if len(users) == 0 else f'(Les participants actuels sont: {pp})'

        m = f'Il n\'y a pas assez de participants pour lancer une session. ' + \
            f'Il faut au moins {min_users} participants pour lancer une session. ' + \
            participants + \
            f'\n*Pour rejoindre la session: `!me <username>`.*' 

        return m
    

    @staticmethod
    def killing_bot() -> str:

        m = f'Le bot s\'arrête faute de participations. 😢' + \
            f'\n\nVous pouvez redémarrer le bot avec `!start`.'
        
        return m
    

    @staticmethod
    def space_padding(string: str, length: int) -> str: 

        return '`' + string + ' ' * (length - len(string)) + '`'

        
