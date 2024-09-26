from typing import Optional
from src.persistence.models.contribution import Contribution
from src.persistence.models.session import Session


class SessionDbResource:

    def __init__(self, session):
        self.session = session


    def create_session(self, session: Session):

        with self.session() as _session:

            _session.add(session)
            _session.commit()
            _session.refresh(session)

    def get_active_session(self, channel_id: int) -> Optional[Session]:

        with self.session() as session:

            return session.query(Session).filter(Session.channel_id == channel_id, Session.is_active == True).first()
        
    def get_last_session_number(self, channel_id: int):

        with self.session() as session:

            last_session = session.query(Session).filter(Session.channel_id == channel_id).order_by(Session.session_number.desc()).first()
            return last_session.session_number if last_session else 0
        

    def get_last_active_session_number(self, channel_id: int) -> int:

        with self.session() as session:
            last_contribution: Contribution = session.query(Contribution).filter(Contribution.channel_id == channel_id).order_by(Contribution.id.desc()).first()
            corresponding_session: Session = session.query(Session).filter(Session.id == last_contribution.session_id).first() if last_contribution else None
            return corresponding_session.session_number if corresponding_session else 0


    def set_session_inactive(self, session: Session):

        with self.session() as _session:

            merged_session = _session.merge(session)
            merged_session.is_active = False
            _session.commit()
            _session.refresh(merged_session)

    
    def update_session(self, session: Session):

        with self.session() as _session:

            updated_session = _session.merge(session)
            _session.commit()
            _session.refresh(updated_session)


    def create_contributions(self, contributions: list[Contribution]):

        if len(contributions) == 0: return

        with self.session() as session:

            session.add_all(contributions)
            session.commit()
            for contribution in contributions:
                session.refresh(contribution)

    def create_contribution(self, contribution: Contribution):

        with self.session() as session:

            session.add(contribution)
            session.commit()
            session.refresh(contribution)


    def get_contributions(self, session_id: int):

        with self.session() as session:

            return session.query(Contribution).filter(Contribution.session_id == session_id).all()
        

    def update_contribution(self, contribution: Contribution):

        with self.session() as session:

            updated_contribution = session.merge(contribution)
            session.commit()
            session.refresh(updated_contribution)


    def get_user_contributions(self, discord_id: int, channel_id: int):

        with self.session() as session:

            return session.query(Contribution).filter(Contribution.user_discord_id == discord_id, Contribution.channel_id == channel_id).all()


    def get_sessions(self, session_ids: list[int]) -> list[Session]:

        with self.session() as session:

            return session.query(Session).filter(Session.id.in_(session_ids)).all()