from sqlalchemy import JSON, TIMESTAMP, Column, String, BigInteger, Integer, Boolean
from src.persistence.models.base import Base

class Contribution(Base):

    __tablename__ = 'contributions'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    message_id = Column(BigInteger)
    channel_id = Column(BigInteger)
    session_id = Column(BigInteger)
    platform = Column(String(255))
    content = Column(String(255))
    anonymous = Column(Boolean)
    timestamp = Column(TIMESTAMP(timezone=True))
    settings = Column(JSON, default={})
    reacts = Column(JSON, default={})
    points = Column(Integer, default=0)
    winner = Column(Boolean, default=False)
    banger = Column(Boolean, default=False)


    def __init__(self, user_id, message_id, channel_id, session_id, content, anonymous, platform, timestamp):

        self.user_id = user_id
        self.session_id = session_id
        self.message_id = message_id
        self.channel_id = channel_id
        self.anonymous = anonymous
        self.content = content
        self.platform = platform
        self.timestamp = timestamp


    def __repr__(self):
        return f'<Contribution {self.id} - {self.content}>'
