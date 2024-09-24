import json
from src.data.badges import BADGES
from src.data.genres import SUBGENRES
from src.models.music import GenreName, Theme
from src.persistence.database import DatabaseAccess
from src.persistence.models.contribution import Contribution
from src.persistence.models.user import User

from src.models.badge import Badge

class Badger:

    @staticmethod
    def assign_badges(user: User, db: DatabaseAccess) -> list[Badge]:

        contributions: list[Contribution] = db.session_resource.get_user_contributions(user.discord_id)
        contributions_sessions_ids = [contribution.session_id for contribution in contributions]
        sessions = db.session_resource.get_sessions(contributions_sessions_ids)

        # Get themes 
        themes: list[Theme] = [Theme.fromdict(json.loads(session.theme)) for session in sessions]
        
        # Dict with session count for each genre inside themes
        genre_count: dict[GenreName, int] = {genre: 0 for genre in GenreName}
        subgenre_count: dict[str, int] = {subgenre.name: 0 for subgenre in SUBGENRES}
        challenge_count: int = 0

        # Theme count
        for theme in themes:
            if theme.type == 'Genre':
                genre_count[theme.content.name] += 1
            elif theme.type == 'SubGenre':
                genre_count[theme.content.genre.name] += 1
                subgenre_count[theme.content.name] += 1
            elif theme.type == 'Challenge':
                challenge_count += 1

        awarded_badges: list[Badge] = []
        for badge in BADGES:

            if badge.name == 'Early Bird':
                if user.id <= 10: awarded_badges.append(badge)
            
            elif badge.name == 'Streaker':
                count = {'Bronze': 5, 'Silver': 10, 'Gold': 25, 'Platinum': 50}.get(badge.metal)
                if user.streak >= count: awarded_badges.append(badge)
            
            elif badge.name == 'Veteran':
                count = {'Bronze': 10, 'Silver': 25, 'Gold': 50, 'Platinum': 100}.get(badge.metal)
                if len(contributions) >= count: awarded_badges.append(badge)
            
            elif badge.name == 'Eclectic':

                if badge.metal in ['Bronze', 'Silver']:
                    count = {'Bronze': 5, 'Silver': 10}.get(badge.metal)
                    if len([g for g in genre_count if genre_count[g] > 0]) >= count: awarded_badges.append(badge)

                elif badge.metal in ['Gold', 'Platinum']:
                    count = {'Gold': 15, 'Platinum': 20}.get(badge.metal)
                    if len([sg for sg in subgenre_count if subgenre_count[sg] > 0]) >= count: awarded_badges.append(badge)
            
            elif 'Specialist' in badge.name: 

                badge_to_genre = {
                    'House Specialist': GenreName.HOUSE,
                    'Techno Specialist': GenreName.TECHNO,
                    'Disco Specialist': GenreName.DISCO,
                    'Electronic Specialist': GenreName.ELECTRONIC,
                    'Reggae Specialist': GenreName.REGGAE,
                    'Rock Specialist': GenreName.ROCK,
                }

                count = {'Bronze': 5, 'Silver': 10, 'Gold': 25, 'Platinum': 50}.get(badge.metal)
                if genre_count[badge_to_genre[badge.name]] >= count: awarded_badges.append(badge)
        
        return awarded_badges

