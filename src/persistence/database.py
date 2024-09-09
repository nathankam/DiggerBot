from src.persistence.repositories.session_repository import SessionDbResource
from src.persistence.repositories.group_repository import GroupDbResource
from src.persistence.models.base import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import json
from functools import partial


class DatabaseAccess: 

    def __init__(self, db_uri: str):

        self.engine = create_engine(
            db_uri, future=True, 
            json_serializer=partial(json.dumps, ensure_ascii=False),
        )

        # Create a Session class 
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

        # Repositories 
        self.session_resource = SessionDbResource(self.Session)
        self.group_resource = GroupDbResource(self.Session)


    def get_engine(self):
        return self.engine