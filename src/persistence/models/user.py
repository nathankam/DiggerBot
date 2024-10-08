from sqlalchemy import JSON, Column, Integer, String, BigInteger, DateTime, Boolean
from src.persistence.models.base import Base

class User(Base):

    __tablename__ = 'users'

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    discord_id = Column(BigInteger)
    group_id = Column(BigInteger)
    dm_channel_id = Column(BigInteger, default=None)
    points = Column(Integer, default=0)
    streak = Column(BigInteger, default=0)
    best_streak = Column(BigInteger, default=0)
    last_participation = Column(Integer, default=0)
    frozen = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    settings = Column(JSON, default={})
    admin = Column(Boolean, default=False)


    def __init__(self, discord_id, group_id, name):

        self.id = f'{group_id}-{discord_id}'
        self.discord_id = discord_id
        self.group_id = group_id
        self.name = name


    def __repr__(self):
        return f'<User {self.id} - {self.name}>'

