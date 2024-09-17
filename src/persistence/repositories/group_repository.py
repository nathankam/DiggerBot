from src.persistence.models.group import Group
from src.persistence.models.user import User


class GroupDbResource:

    def __init__(self, session):
        self.session = session


    def create_group(self, group: Group):

        with self.session() as session:

            session.add(group)
            session.commit()
            session.refresh(group)


    def update_group(self, group: Group):

        with self.session() as session:
            updated_group = session.merge(group)
            session.commit()
            session.refresh(updated_group)


    def get_groups(self):

        with self.session() as session:

            return session.query(Group).all()
        

    def get_group(self, group_id: int):

        with self.session() as session:

            return session.query(Group).filter(Group.id == group_id).first()
        

    def get_group_by_channel_id(self, channel_id: int):

        with self.session() as session:

            return session.query(Group).filter(Group.channel_id == channel_id).first()
        
    
    def add_user_to_group(self, group: Group, user_id: int):

        with self.session() as session:

            group.users.append(user_id)
            session.commit()
            session.refresh(group)


    def get_user_by_id(self, discord_id: int, group_id: int):

        with self.session() as session:

            return session.query(User).filter(User.id == f'{group_id}-{discord_id}').first()
        

    def get_group_users(self, group_id: int):

        with self.session() as session:

            return session.query(User).filter(User.group_id == group_id).all()
        

    def get_user_by_username(self, username: str, group_id: int):
            
            with self.session() as session:
    
                return session.query(User).filter(User.name == username, User.group_id == group_id).first()
        
    def update_user(self, user: User):

        with self.session() as session:
            updated_user = session.merge(user)
            session.commit()
            session.refresh(updated_user)


    def add_user(self, user: User):

        with self.session() as session:

            session.add(user)
            session.commit()
            session.refresh(user)

            
    def remove_user_from_group(self, group: Group, user_id: int):

        with self.session() as session:

            group.users.remove(user_id)
            session.commit()
            session.refresh(group)
        

    def remove_user(self, user: User):

        with self.session() as session:

            session.delete(user)
            session.commit()
            session.refresh(user)


    def modify_schedule(self, group: Group, schedule_id: int):

        with self.session() as session:

            group.schedule_id = schedule_id
            session.commit()
            session.refresh(group)

    
    def streak_reset(self, group: Group):

        with self.session() as session:

            updated_group = session.merge(group)
            updated_group.streak = 0 
            session.commit()
            session.refresh(updated_group)


    def streak_increment(self, group: Group):

        with self.session() as session:

            updated_group = session.merge(group)
            updated_group.streak += 1
            session.commit()
            session.refresh(updated_group)
