from sqlalchemy import JSON, Column, String, BigInteger, DateTime, Boolean
from src.persistence.models.base import Base

import datetime

class Group(Base):

    __tablename__ = 'groups'

    id = Column(BigInteger, primary_key=True)
    group_id = Column(String(255))
    name = Column(String(255))
    users = Column(JSON, default=[])
    settings = Column(JSON, default={})
    schedule_id = Column(BigInteger, default=1)
    created_at = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)


    def __init__(self, group_id, name):

        self.group_id = group_id
        self.name = name


    def __repr__(self):
        return f'<Group {self.id} - {self.name}>'