from sqlalchemy import JSON, TIMESTAMP, Column, String, BigInteger, Integer, Boolean
from src.persistence.models.base import Base

class UserBadge(Base):

    __tablename__ = 'badges'

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
    emoji = Column(String(255))
    user_id = Column(String(255))
    discord_id = Column(BigInteger)
    group_id = Column(BigInteger)
    assigned = Column(TIMESTAMP(timezone=True))

    def __init__(self, badge_name, badge_metal, description, emoji, user_id, discord_id, group_id):

        self.id = f'{user_id}-{badge_name}-{badge_metal}'
        self.name = f'{badge_name}-{badge_metal}'
        self.description = description
        self.emoji = emoji
        self.user_id = user_id
        self.discord_id = discord_id
        self.group_id = group_id




