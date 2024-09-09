from sqlalchemy import JSON, Column, String, BigInteger, Integer, DateTime, Boolean
from src.persistence.models.base import Base

class Contribution(Base):

    __tablename__ = 'contributions'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    message_id = Column(BigInteger)
    session_id = Column(String(255))
    group_id = Column(String(255))
    platform = Column(String(255))
    content = Column(String(255))
    timestamp = Column(DateTime)
    settings = Column(JSON, default={})
    reacts = Column(JSON, default={})
    points = Column(Integer, default=0)
    winner = Column(Boolean, default=False)
    banger = Column(Boolean, default=False)


    def __init__(self, user_id, message_id, session_id, content, platform, timestamp):

        self.user_id = user_id
        self.session_id = session_id
        self.message_id = message_id
        self.content = content
        self.platform = platform
        self.timestamp = timestamp


    def __repr__(self):
        return f'<Contribution {self.id} - {self.content}>'
