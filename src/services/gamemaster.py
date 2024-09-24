from dataclasses import dataclass
from typing import Literal, Optional
import pytz
import random

from src.data.greetings import GREETINGS, BRAVO
from src.data.reacts import REACTS
from src.models.badge import Badge
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
        m_fr = f'**[SESSION {session.session_number} / START]**' + \
            f'\n\n{random.choice(GREETINGS[group.language])}' + \
            f'\n\nLe thème d\'aujourd\'hui est: **{theme_name}** \n*{theme.content.description}*' + \
            f'\n\nVous avez jusqu\'à **{TRANSLATIONS[indicator]} {vote_hour}** pour proposer une track!'
        
        m_en = f'**[SESSION {session.session_number} / START]**' + \
            f'\n\n{random.choice(GREETINGS[group.language])}' + \
            f'\n\nToday\'s theme is: **{theme_name}** \n*{theme.content.description}*' + \
            f'\n\nYou have until **{TRANSLATIONS[indicator]} {vote_hour}** to propose a track!'
        

        # Session Start
        return {'FR': m_fr, 'EN':  m_en}[group.language]
    

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

        m_fr = f'**[SESSION {session.session_number} (G{group.id}) / START]**' + \
            f'\n\nLa session est en mode incognito 🥸.' + \
            f'\nTu peux partager ton lien ici, **en répondant à ce message** ↩, et je m\'occupe du reste!' + \
            f'\n\nThème: {theme_name} \n*{theme.content.description}*' + \
            f'\n\nTu as jusqu\'à **{TRANSLATIONS[indicator]} {vote_hour}** pour proposer une track!'
        
        m_en = f'**[SESSION {session.session_number} (G{group.id}) / START]**' + \
            f'\n\nThe session is in incognito mode 🥸.' + \
            f'\nYou can share your link here, **by replying to this message** ↩, and I\'ll take care of the rest!' + \
            f'\n\nTheme: {theme_name} \n*{theme.content.description}*' + \
            f'\n\nYou have until **{TRANSLATIONS[indicator]} {vote_hour}** to propose a track!'
        
        return {'FR': m_fr, 'EN':  m_en}[group.language]
    
        
    @staticmethod
    def close_participation(session: Session, contributions: list[Contribution], streaks: dict, group: Group) -> str: 

        # Pytz
        tz = pytz.timezone(group.timezone)
        now = session.vote_at.astimezone(tz)
        end_time = session.end_at.astimezone(tz)
        indicator = GameMaster.get_day_indicator(now, end_time)
        end_hour = end_time.strftime('%H:%M')

        # Users
        users = f'\n\n' + f'\n'.join([f'{GameMaster.space_padding(u, 20)} - *Streak:* ***{s}***' for u, s in streaks.items()])

        cont = {
            'FR': f'participation a été enregistrée.' if len(contributions) == 1 else f'participations ont été enregistrées.',
            'EN': f'participation has been recorded.' if len(contributions) == 1 else f'participations have been recorded.'
        }[group.language]

        m_fr = f'**[SESSION {session.session_number} / VOTE]**' + \
            f'\n\nLes participations sont closes! {len(contributions)} {cont}' + \
            (users if not session.incognito else '') + \
            f'\n\nToutes les reacts comptent comme un vote! Vous pouvez aussui utilisez des votes spécifiques: \n' + \
            f'\n'.join([f' {a.emoji} - *{a.meaning}*' for a in REACTS]) + \
            f'\n\nVous avez jusqu\'à {TRANSLATIONS[indicator]} {end_hour} pour voter!'
        
        m_en = f'**[SESSION {session.session_number} / VOTE]**' + \
            f'\n\nParticipations are closed! {len(contributions)} {cont}' + \
            (users if not session.incognito else '') + \
            f'\n\nAll emoji react count as a vote! You can also use special reacts: \n' + \
            f'\n'.join([f' {a.emoji} - *{a.meaning}*' for a in REACTS]) + \
            f'\n\nYou have until {TRANSLATIONS[indicator]} {end_hour} to vote!'
        
        return {'FR': m_fr, 'EN':  m_en}[group.language]
    

    @staticmethod
    def anonymous_contributions(anonymous_contributions: list[Contribution]) -> Optional[list[str]]:

        messages = []
        for c in anonymous_contributions:
            messages.append(f'🥸 [ANONYMOUS CONTRIBUTION] -- {c.content}')

        return messages
    

    @staticmethod
    def close_votes(session: Session, group: Group, users: list[User], votes: dict, winners: list) -> str: 

        # Winners translation
        winners_dict = {u.discord_id: u.name for u in users}
        winners_names = [winners_dict.get(w, 'unknown') for w in winners]

        # Voters List
        voters = '\n'.join([f'- **{user}**  *{vote_count} votes*' for user, vote_count in votes.items() if vote_count > 0])

        vote_msg = {
            'FR': 'vote a été enregistré.' if len(votes) == 1 else 'votes ont été enregistrés.',
            'EN': 'vote has been recorded.' if len(votes) == 1 else 'votes have been recorded.',
        }[group.language]

        win_msg = {
            'FR': f'Le gagnant d\'aujourd\'hui est: *{winners_names[0]}*',
            'EN': f'Today\'s winner is: *{winners_names[0]}*'  
        }[group.language] if len(winners) == 1 else {
            'FR': f'Les gagnants d\'aujourd\'hui sont: ' + ', '.join(winners_names),
            'EN': f'Today\'s winners are: ' + ', '.join(winners_names)
        }[group.language]

        m_fr = f'**[SESSION {session.session_number} / RESULTS]**' + \
            f'\n\nLes votes sont clos! {len(votes)} {vote_msg}' + \
            f'\n\n{voters}' + \
            F'\n{win_msg}' + \
            f'\n\n{random.choice(BRAVO[group.language])}'
        
        m_en = f'**[SESSION {session.session_number} / RESULTS]**' + \
            f'\n\nVotes are closed! {len(votes)} {vote_msg}' + \
            f'\n\n{voters}' + \
            f'\n{win_msg}' + \
            f'\n\n{random.choice(BRAVO[group.language])}'
        
        return {'FR': m_fr, 'EN':  m_en}[group.language]
    

    @staticmethod
    def badges_assigned(user: User, badges: list[Badge]) -> list[str]: 

        mlist = []
        for badge in badges: 
            badge_name = badge.emoji +  (f'{badge.metal} ' if badge.metal else '') + badge.name 
            m = f'**[BADGE]** - **{user.name}** won the badge ***{badge_name}***' 
            mlist.append(m)

        return mlist
    

    @staticmethod
    def welcome(language: Literal['EN', 'FR']) -> str: 

        m_fr = f'\n**Bienvenue!** 🎶' + \
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
            f'\n\n`!help` *pour plus d\'infos sur comment interragir avec mes paramètres.*' + \
            f'\n`!lang EN` *to switch to english.*' + \
            f'\n\n🎷🎶🎧'
        
        
        m_en = f'\n**Welcome!** 🎶' + \
            f'\n- I am DiggerBot, music enthusiast, always looking for new tunes! ' + \
            f'The goal of this group is to collaborate to discover new gems. ' + \
            f'\n- At each session, I propose a theme and the members of the group are free to participate by sharing a Spotify, Youtube or Soundcloud link. ' + \
            f'At the end of the participation time, everyone can react to the contributions of others with reacts that correspond to different types of votes. ' + \
            f'\n- The most voted songs earn points to encourage the most fine explorers and a streak/badges system rewards the most assiduous participants.' + \
            f'Every month, I publish statistics on the sessions, create a Spotify playlist with the best songs of the month and award the *Digger-of-the-Month* Award.' + \
            f'\n- As each group is unique, you can customize my settings so that I adapt to your preferences.' + \
            f'For example, you can change the sessions frequency by selecting a *schedule*, ' + \
            f'or change the frequency at which each musical genre is proposed...' + \
            f'\n\nTo start, type `!me <username>` to create a profile with your name.' + \
            f'\n\n`!help` *for more info on how to interact with my settings.*\n'

        return {'FR': m_fr, 'EN':  m_en}[language]
    

    @staticmethod
    def welcome_user(group_name: str, user_name: str, language: Literal['EN', 'FR']) -> str:

        m_fr = f'Hello **{user_name}**!' + \
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
        
        m_en = f'Hello **{user_name}**!' + \
            f'\nYou have been added to the group ***{group_name}***! Let me give you a little reminder on how the group works: ' + \
            f'\n- At each session, I propose a theme and the members of the group are free to participate by sharing a Spotify, Youtube or Soundcloud link. ' + \
            f'At the end of the time for contributions, everyone can react to the links shared by others with reacts that correspond to different types of votes. ' + \
            f'The most voted songs earn points to encourage finest explorers and a streak/badges system rewards the most assiduous participants. ' + \
            f'Every month, I publish statistics on the sessions, create a Spotify playlist with the best songs of the month and award the *Digger-of-the-Month Award*.' + \
            f'\n- As each group is unique, you can customize my settings to fit your preferences. ' + \
            f'For example, you can change the sessions frequency by selecting a *schedule*, ' + \
            f'or change the frequency at which each musical genre is proposed...' + \
            f'\n- I only communicate in the general channel, but if the group goes incognito, you will be able to share your contribution privately here and I will transmit it in the general channel to keep it anonymous' + \
            f'\n\nThere you go, you know everything! Can\'t wait to listen to what you\'ll share! 🎷\n'
            
        return {'FR': m_fr, 'EN':  m_en}[language]
    

    @staticmethod
    def get_day_indicator(datetime_now, datetime_next): 

        if datetime_now.day == datetime_next.day:
            return 'today'
        elif datetime_next.day - datetime_now.day == 1:
            return 'tomorrow'
        else:
            return datetime_next.strftime("%A").lower()

    
    @staticmethod
    def incognito_on(language: Literal['FR', 'EN']) -> str: 

        m_fr = f'**[INFO]** ' + \
            f'*Le groupe est passé en mode incognito!*' + \
            f'\nÀ partir de maintenant, partage tes liens ici et je les transmettrai dans le groupe pour que ta contribution reste anonyme. 🥸\n'
        
        m_en = f'**[INFO]** ' + \
            f'*The group is now in incognito mode!*' + \
            f'\nFrom now on, share your links here and I will transmit them in the group so that your contribution remains anonymous. 🥸\n'

        return {'FR': m_fr, 'EN':  m_en}[language]


    @staticmethod
    def incognito_off(language: Literal['FR', 'EN']) -> str: 

        m_fr = f'**[INFO]** ' + \
            f'*Le groupe n\'est plus en mode incognito!*' + \
            f'\nÀ partir de maintenant, partage tes liens directement dans le canal général. 🎶\n'
        
        m_en = f'**[INFO]** ' + \
            f'*The group is no longer in incognito mode!*' + \
            f'\nFrom now on, share your links directly in the general channel. 🎶\n'

        return {'FR': m_fr, 'EN':  m_en}[language]

    
    @staticmethod
    def no_contributions(session: Session, group: Group, participation_timeout: int) -> str: 

        m_fr = f'**[SESSION {session.session_number} / END]**' + \
            f'\n\nAucune participation n\'a été enregistrée. ' + \
            f'Vous pouvez diminuer la fréquence des sessions en modifiant le schedule avec `!schedule_set <schedule_id>`. Listez la liste des schedules avec `!schedule_list`.' + \
            f"\n\n*Le bot s'arrêtera d'ici {participation_timeout} session(s) si aucune participation n'est enregistrée.*"
        
        m_en = f'**[SESSION {session.session_number} / END]**' + \
            f'\n\nNo contributions were recorded. ' + \
            f'You can decrease the frequency of the sessions by modifying the schedule with `!schedule_set <schedule_id>`. List the schedules with `!schedule_list`.' + \
            f"\n\n*The bot will stop in {participation_timeout} session(s) if no contributions are recorded.*"

        return {'FR': m_fr, 'EN':  m_en}[group.language]
    

    @staticmethod
    def not_enough_users(users: list[User], group: Group, min_users: int) -> str: 

        pp = ', '.join([u.name for u in users])
        participants = {
            'FR': f'(Aucun utilisateur enregistré.)',
            'EN': f'(No registered users.)',
        }[group.language] if len(users) == 0 else {
            'FR': f'(Les participants actuels sont: {pp})',
            'EN': f'(Current participants are: {pp})'
        }[group.language]

        m_fr = f'**[INFO]** ' + \
            f'Il n\'y a pas assez de participants pour lancer une session. ' + \
            f'Il faut au moins {min_users} participants pour lancer une session. ' + \
            participants + \
            f'\n*Pour rejoindre la session: `!me <username>`.*' 
        
        m_en = f'**[INFO]** ' + \
            f'There are not enough participants to start a session. ' + \
            f'You need at least {min_users} participants to start a session. ' + \
            participants + \
            f'\n*To join the session: `!me <username>`.*'

        return {'FR': m_fr, 'EN':  m_en}[group.language]
    

    @staticmethod
    def killing_bot(language: Literal['EN', 'FR']) -> str:

        m_fr = f'**[INFO]** ' + \
            f'Le bot s\'arrête faute de participations. 😢' + \
            f'\n\nVous pouvez redémarrer le bot avec `!start`.'
        
        m_en = f'**[INFO]** ' + \
            f'The bot is stopping due to lack of participation. 😢' + \
            f'\n\nYou can restart the bot with `!start`.'
        
        return {'FR': m_fr, 'EN':  m_en}[language]
    

    @staticmethod
    def space_padding(string: str, length: int) -> str: 

        return '`' + string + ' ' * (length - len(string)) + '`'

        
