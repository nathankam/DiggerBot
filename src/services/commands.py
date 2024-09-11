import asyncio
import traceback
import json
from typing import Optional

import discord
from src.data.commands import COMMANDS
from src.data.schedules import SCHEDULES
from src.models.message import Command
from src.models.music import GenreName
from src.models.settings import Settings
from src.persistence.database import DatabaseAccess
from src.persistence.models.group import Group
from src.persistence.models.user import User
from src.services.bot import DiscordBot


class CommandCenter:

    def __init__(self, bot: DiscordBot, group_id: int):

        self.bot: DiscordBot = bot
        self.group_id: int = group_id

    def execute(self, content: str, discord_id: int, command: Command, db_access: DatabaseAccess) -> str:

        print(f'[LOG] --- Executing command {command.code} for group {self.group_id}')
        user: Optional[User] = db_access.group_resource.get_user_by_id(discord_id, self.group_id)

        # Blocking command
        message, block = self.block_command(command, user)
        if block: return message

        # HELP
        if command.code == '!help':

            message = self.title(command, 'Available commands')
            commands = '\n'.join([
                f'- **{self.padding_space(c.code, 10)}** *{c.description}*' + (f' / {c.instructions}' if c.instructions else '') 
                for c in COMMANDS])
            message = message + commands


        # ADD USER
        elif command.code == '!user_create':

            try:

                # Creating New User
                username = content.split(' ')[1]
                discord_id = content.split(' ')[2]
                group_users: list[User] = db_access.group_resource.get_group_users(self.group_id)

                if any([u.discord_id == discord_id for u in group_users]):
                    message = self.warning(command, f'User with Messenger ID [{discord_id}] already exists')

                if any([u.name == username for u in group_users]):
                    message = self.warning(command, f'User with name [{username}] already exists')

                else: 
                    # Adding New User 
                    new_user = User(
                        discord_id=discord_id,
                        group_id=self.group_id,
                        name=username
                    )
                    db_access.group_resource.add_user(new_user)

                    message = self.warning(command, f'User {new_user.name} created successfully')
            except Exception as e: 
                message = self.warning(command, f'Error creating user: *{e}*')


        # DELETE USER
        elif command.code == '!user_delete':

            try: 
                # Removing User
                username = content.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = self.warning(command, f'User [{username}] does not exist')
                else:
                    db_access.group_resource.remove_user(user)
                    message = self.warning(command, f'User [{username}] deleted successfully')
            except Exception as e: 
                message = self.warning(command, f'Error deleting user: *{e}*')


        # FREEZE USER
        elif command.code == '!user_freeze':

            try:  
                username = content.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = self.warning(command, f'User [{username}] does not exist')
                else:
                    user.frozen = True
                    db_access.group_resource.update_user(user)
                    message = self.warning(command, f'Freezing user: [{username}]')
            except Exception as e:
                message = self.warning(command, f'Error freezing user: *{e}*')


        # UNFREEZE USER
        elif command.code == '!user_unfreeze':

            try:  
                username = content.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = self.warning(command, f'User [{username}] does not exist')
                else:
                    user.frozen = False
                    db_access.group_resource.update_user(user)
                    message = self.warning(command, f'Unfreezing user: [{username}]')
            except Exception as e:
                message = self.warning(command, f'Error unfreezing user: *{e}*')


        # USER LIST
        elif command.code == '!user_list':

            try: 
                users: list[User] = db_access.group_resource.get_group_users(self.group_id)
                message = self.title(command, 'Users in group')
                users_list = '\n'.join([f'- **{u.name}** - {u.discord_id}' for u in users])
                message = message + users_list
            except Exception as e:
                message = self.warning(command, f'Error listing users: *{e}*')


        # USER POINTS
        elif command.code == '!points':

            try: 
                users: list[User] = db_access.group_resource.get_group_users(self.group_id)
                message = self.title(command, 'User points')
                users_points = '\n'.join([f'- **{u.name}** - {u.points}' for u in users])
                message = message + users_points
            except Exception as e:
                message = self.warning(command, f'Error listing points: *{e}*')


        # GROUP INFO
        elif command.code == '!info':

            try: 
                message = self.title(command, 'Group Info')
                group: Group = db_access.group_resource.get_group(self.group_id)

                schedule_id = group.schedule_id
                schedule = [s for s in SCHEDULES if s.id == schedule_id][0]
                schedule_info = f'- **Schedule**: {schedule.name} - {schedule.description}\n'

                message = message + schedule_info
            except Exception as e:
                message = self.warning(command, f'Error getting group info: *{e}*')

        # LIST SCHEDULES
        elif command.code == '!list_schedules':

            try: 
                message = self.title(command, 'Available schedules')
                schedules = '\n'.join([f'* **{s.id}** - {self.padding_space(s.name, 20)} *{s.description}*' for s in SCHEDULES])
                message = message + schedules
            except Exception as e:
                message = self.warning(command, f'Error listing schedules *{e}*')

        
        # SET SCHEDULE
        elif command.code == '!set_schedule':

            try: 
                schedule_id = content.split(' ')[1]
                available_ids = [s.id for s in SCHEDULES]
                if schedule_id not in available_ids:
                    message = self.warning(command, f'Schedule [{schedule_id}] does not exist')
                else: 
                    group: Group = db_access.group_resource.get_group(self.group_id)
                    group.schedule_id = schedule_id
                    db_access.group_resource.modify_schedule(group, schedule_id)

                    message = self.warning(command, f'Schedule [{schedule_id}] set successfully')
            except Exception as e:
                message = self.warning(command, f'Error setting schedule: *{e}*')


        # ADD USER
        elif command.code == '!goagain':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                group.is_active = True
                db_access.group_resource.update_group(group)
                message = self.warning(command, 'Group is reactivated')
            except Exception as e:
                message = self.warning(command, f'Error reactivating group *{e}*')


        # SETTINGS
        elif command.code == '!settings_show':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                message = settings.show_settings()
            except Exception as e:
                message = self.warning(command, f'Error showing settings: *{e}*')
                print(traceback.format_exc())
 


        # SETTINGS INC
        elif command.code == '!settings_incognito':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                settings.incognito = bool(int(content.split(' ')[1], 0))
                group.settings = json.dumps(settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Incognito mode set to {settings.incognito}')
            except Exception as e:
                message = self.warning(command, f'Error toggling incognito mode *{e}*')

        
        # SETTINGS GER
        elif command.code == '!settings_ger':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                settings.genre_explo_ratio = float(content.split(' ')[1], 0.5)
                group.settings = json.dumps(settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Genre Exploration Ratio set to {settings.genre_explo_ratio}')
            except:
                message = self.warning(command, 'Error setting genre exploration ratio')


        # SETTNGS GSR
        elif command.code == '!settings_gsr':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                settings.genre_subgenre_ratio = float(content.split(' ')[1], 0.5)
                group.settings = json.dumps(settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Genre / Subgenre Ratio set to {settings.genre_subgenre_ratio}')
            except:
                message = self.warning(command, 'Error setting genre/subgenre ratio')


        # SETTINGS GPR
        elif command.code == '!settings_gpr':

            try: 
                args= content.split(' ')
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                genre = GenreName(args[1])
                weight = int(args[2])
                settings.genre_weights[genre] = weight
                group.settings = json.dumps(settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Genre Proportion for {genre.name} set to {weight}')
            except Exception as e:
                message = self.warning(command, f'Error setting genre proportion: *{e}*')
                print(traceback.format_exc())


        # SETTINGS GPR SHOW
        elif command.code == '!settings_sgprop':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                _, genre_proportion = settings.show_genre_reparition()
                message = genre_proportion
            except:
                message = self.warning(command, f'Error showing genre proportions: *{e}*')


        return message
    
    @staticmethod
    def check_commands(messages: list[discord.Message]) -> list[tuple[Command, discord.Message]]:

        commands = []
        for message in reversed(messages):
            for command in COMMANDS:
                if command.code in message.content and not message.author.bot:
                    commands.append((command, message))

        print(f'[LOG] --- Found {len(commands)} commands')
    
        return commands
    
    @staticmethod
    def block_command(command: Command, user: User) -> tuple[str, bool]:

        if command.restricted and user is not None and not user.admin:

            text = 'You do not have permission to use this command'
            message = CommandCenter.warning(command, text)
            return message, True
        
        if command.name != 'ADD USER' and user is None:

            text = 'User need to be registered to use this command'
            message = CommandCenter.warning(command, text)
            return message, False
        
        return '', False
        
    
    @staticmethod
    def title(command: Command, message: str) -> str:
        return f'-- *{command.name}* - **{message}** --\n\n'
    
    @staticmethod
    def warning(command: Command, message: str) -> str:
        return f'*[{command.name}]* - {message}'
    
    @staticmethod   
    def padding_space(message: str, max_space: int) -> str:
        message_length = len(message)
        padding = max_space - message_length
        return message + '  ' * padding
        

