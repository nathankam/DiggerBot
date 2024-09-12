import json
from sqlalchemy import JSON, TIMESTAMP, Column, String, BigInteger, DateTime, Boolean
from src.models.settings import DEFAULT_SETTINGS, Settings
from src.persistence.models.base import Base

import pytz

import datetime

class Group(Base):

    __tablename__ = 'groups'

    id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger)
    name = Column(String(255))
    settings = Column(JSON, default={})
    schedule_id = Column(BigInteger, default=1)
    timezone = Column(String(255), default='Europe/Paris')
    last_check = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(pytz.UTC))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(pytz.UTC))
    is_active = Column(Boolean, default=True)


    def __init__(self, channel_id, name, timezone: str = 'Europe/Paris', settings: Settings = DEFAULT_SETTINGS):

        self.channel_id = channel_id
        self.name = name
        self.timezone = timezone
        self.settings = json.dumps(settings.to_dict())


    def __repr__(self):
        return f'<Group {self.id} - {self.name}>'