import asyncio
from src.data.commands import COMMANDS
from src.data.schedules import SCHEDULES
from src.models.message import Command
from src.persistence.database import DatabaseAccess
from src.persistence.models.group import Group
from src.persistence.models.user import User
from src.services.discord import DiscordBot
from src.services.messenger import MessengerBot


class CommandCenter:

    def __init__(self, bot: DiscordBot, group_id: int, user_id: int):

        self.bot: DiscordBot = bot
        self.group_id: int = group_id

    def execute(self, message: str, user_id: int, command: Command, db_access: DatabaseAccess):

        user: User = db_access.group_resource.get_user_by_id(user_id, self.group_id)

        if command.restricted and not user.admin:

            message = f'[{command.name}] -- You do not have permission to use this command'
            asyncio.run(self.bot.send_message(
                message=message, 
                channel_id=self.group_id
            ))
            return

        if command.code == '!help':

            message = f'[{command.name}] -- Available commands:\n\n'
            commands = '\n'.join([f'{c.code} / {c.description}' + (f' / {c.instructions}' if c.instructions else '') for c in COMMANDS])
            message = message + commands


        elif command.code == '!user_create':

            username = message.split(' ')[1]
            messenger_id = message.split(' ')[2]

            try:

                # Check if user already exists / username already taken
                group_users: list[User] = db_access.group_resource.get_group_users(self.group_id)
                if any([u.messenger_id == messenger_id for u in group_users]):
                    message = f'[{command.name}] -- User with Messenger ID [{messenger_id}] already exists'

                if any([u.name == username for u in group_users]):
                    message = f'[{command.name}] -- User with username [{username}] already exists'

                else: 
                    # Adding New User 
                    new_user = User(
                        messenger_id=messenger_id,
                        name=username, 
                        group_id=self.group_id
                    )
                    db_access.group_resource.add_user(new_user)

                    message = f'[{command.name}] -- User {new_user.name} created successfully'
            except: 
                message = f'[{command.name}] -- Error creating user'


        elif command.code == '!user_delete':

            try: 
                # Removing User
                username = message.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = f'[{command.name}] -- User [{username}] does not exist'
                else:
                    db_access.group_resource.remove_user(user)
                    message = f'[{command.name}] -- User [{username}] deleted successfully'
            except: 
                message = f'[{command.name}] -- Error deleting user'

        elif command.code == '!user_freeze':

            try:  
                username = message.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = f'[{command.name}] -- User [{username}] does not exist'
                else:
                    user.frozen = True
                    db_access.group_resource.update_user(user)
                    message = f'[{command.name}] -- Freezing user: [{username}]'
            except:
                message = f'[{command.name}] -- Error freezing user'

        elif command.code == '!user_unfreeze':

            try:  
                username = message.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = f'[{command.name}] -- User [{username}] does not exist'
                else:
                    user.frozen = False
                    db_access.group_resource.update_user(user)
                    message = f'[{command.name}] -- Unfreezing user: [{username}]'
            except:
                message = f'[{command.name}] -- Error unfreezing user'


        elif command.code == '!user_list':

            try: 
                users: list[User] = db_access.group_resource.get_group_users(self.group_id)
                message = f'[{command.name}] -- Users in group:\n\n'
                users_list = '\n'.join([f'{u.name} / {u.messenger_id}' for u in users])
                message = message + users_list
            except:
                message = f'[{command.name}] -- Error listing users'

        elif command.code == '!points':

            try: 
                users: list[User] = db_access.group_resource.get_group_users(self.group_id)
                message = f'[{command.name}] -- Showing user points\n\n'
                users_points = '\n'.join([f'{u.name} / {u.points}' for u in users])
                message = message + users_points
            except:
                message = f'[{command.name}] -- Error showing user points'

        elif command.code == '!info':

            try: 

                message = f'[{command.name}] -- Group Info\n\n'
                group: Group = db_access.group_resource.get_group(self.group_id)

                schedule_id = group.schedule_id
                schedule = [s for s in SCHEDULES if s.id == schedule_id][0]
                schedule_info = f'Schedule: {schedule.name} - {schedule.description}\n'

                message = message + schedule_info
            except:
                message = f'[{command.name}] -- Error getting group info'

        elif command.code == '!list_schedules':

            try: 
                message = f'[{command.name}] -- Available schedules:\n\n'
                schedules = '\n'.join([f'{s.id} / {s.name} \n {s.description}' for s in SCHEDULES])
                message = message + schedules
            except: 
                message = f'[{command.name}] -- Error listing schedules'

        elif command.code == '!set_schedule':

            try: 
                schedule_id = message.split(' ')[1]
                available_ids = [s.id for s in SCHEDULES]
                if schedule_id not in available_ids:
                    message = f'[{command.name}] -- Schedule [{schedule_id}] does not exist'
                else: 
                    group: Group = db_access.group_resource.get_group(self.group_id)
                    group.schedule_id = schedule_id
                    db_access.group_resource.modify_schedule(group, schedule_id)

                    message = f'[{command.name}] -- Setting schedule: {schedule_id}'
            except:
                message = f'[{command.name}] -- Error setting schedule'

        elif command.code == '!goagain':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                group.is_active = True
                db_access.group_resource.update_group(group)
                message = f'[{command.name}] -- Group is reactivated'
            except:
                message = f'[{command.name}] -- Error restarting group'


        asyncio.run(self.bot.send_message(
            message=message, 
            channel_id=self.group_id
        ))
        

