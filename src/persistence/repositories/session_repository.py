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

    def get_active_session(self, group_id: str) -> Optional[Session]:

        with self.session() as session:

            return session.query(Session).filter(Session.group_id == group_id, Session.is_active == True).first()
        
    def get_last_session_number(self, group_id: str):

        with self.session() as session:

            return session.query(Session).filter(Session.group_id == group_id).order_by(Session.session_number.desc()).first().session_number
        

    def get_last_active_session_number(self, group_id: str):

        with self.session() as session:
            last_contribution: Contribution = session.query(Contribution).filter(Contribution.group_id == group_id).order_by(Contribution.id.desc()).first()
            return session.query(Session).filter(Session.id == last_contribution.session_id).first().session_number

    def set_session_inactive(self, session: Session):

        with self.session() as _session:

            session.is_active = False
            _session.commit()
            _session.refresh(session)


    def create_contributions(self, contributions: list[Contribution]):

        with self.session() as session:

            session.add_all(contributions)
            session.commit()
            session.refresh(contributions)


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

            session.commit()
            session.refresh(contribution)
