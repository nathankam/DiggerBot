from sqlalchemy import JSON, TIMESTAMP, Column, String, BigInteger, DateTime, Boolean
from src.persistence.models.base import Base

class Session(Base):

    __tablename__ = 'sessions'

    id = Column(BigInteger, primary_key=True)
    session_number = Column(BigInteger)
    channel_id = Column(BigInteger)
    theme = Column(JSON)
    schedule_id = Column(BigInteger)
    start_at = Column(TIMESTAMP(timezone=True))
    vote_at = Column(TIMESTAMP(timezone=True))
    end_at = Column(TIMESTAMP(timezone=True))
    incognito = Column(Boolean, default=False)
    participants = Column(JSON, default=[])
    voters = Column(JSON, default=[])
    winners = Column(JSON, default=[])
    is_active = Column(Boolean, default=True)


    def __init__(self, channel_id, theme, schedule_id, session_number, start_at, vote_at, end_at, incognito=False):

        self.channel_id = channel_id
        self.schedule_id = schedule_id
        self.session_number = session_number
        self.theme = theme
        self.start_at = start_at
        self.vote_at = vote_at
        self.end_at = end_at
        self.incognito = incognito


    def __repr__(self):
        return f'<Session {self.id}>'





