from sqlalchemy import JSON, Column, Integer, String, BigInteger, DateTime, Boolean
from src.persistence.models.base import Base

import datetime

class User(Base):

    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    messenger_id = Column(String(255))
    group_id = Column(String(255))
    name = Column(String(255))
    points = Column(Integer, default=0)
    streak = Column(BigInteger, default=0)
    last_participation = Column(Integer, default=0)
    frozen = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    settings = Column(JSON, default={})
    admin = Column(Boolean, default=False)


    def __init__(self, messenger_id, group_id, name):

        self.id = f'{group_id}-{messenger_id}'
        self.messenger_id = messenger_id
        self.group_id = group_id
        self.name = name


    def __repr__(self):
        return f'<User {self.id} - {self.name}>'

