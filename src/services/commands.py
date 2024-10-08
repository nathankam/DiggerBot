import dataclasses
import re
import traceback
import json
from typing import Any, Optional

import discord
import pytz
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

    def execute(self, content: str, discord_id: int, command: Command, db_access: DatabaseAccess) -> tuple[str, bool, dict]:

        print(f'[LOG] --- Executing command {command.code} for group {self.group_id}')
        user: Optional[User] = db_access.group_resource.get_user_by_id(discord_id, self.group_id)
        success, data = True, {}

        # Checking command
        content = re.sub(r'\s+', ' ', content)
        message, block = self.block_command(command, user)
        if block: return message, False

        # HELP
        if command.code == '!help':

            message = self.title(command, 'Available commands:')
            commands = '\n'.join([
                f'`{self.padding_space(c.instructions if c.instructions else c.code, 20)}`' + f' -- {c.description}' 
                for c in COMMANDS])
            message = message + commands 

        # LANGUAGE
        elif command.code == '!lang':

            try:
                language = content.split(' ')[1]
                if language not in ['FR', 'EN']:
                    message = self.warning(command, 'Invalid language, available languages: FR / EN')
                    success = False
                else: 
                    group: Group = db_access.group_resource.get_group(self.group_id)
                    group.language = language
                    db_access.group_resource.update_group(group)
                    message = self.warning(command, f'Language set to {language}')
            except Exception as e: 
                message = self.warning(command, f'Error setting language *{e}*')
                success = False

        # TIMEZONE
        elif command.code == '!tz':

            try:
                timezone = content.split(' ')[1]
                if timezone not in pytz.all_timezones:
                    message = self.warning(command, 'Invalid <timezone> argument.')
                    success = False
                else:              
                    group: Group = db_access.group_resource.get_group(self.group_id)
                    group.timezone = timezone
                    db_access.group_resource.update_group(group)
                    message = self.warning(command, f'Timezone set to {timezone}')
            except Exception as e: 
                message = self.warning(command, f'Error setting timezone *{e}*')
                success = False

        # ME 
        elif command.code == '!me':

            username = content.split(' ')[1]

            try: 
                username = self.format_username(content.split(' ')[1])
                message, success, data = self.create_user(db_access, discord_id, username, command)
            except Exception as e: 
                message = self.warning(command, f'Error creating user: *{e}*')
                success = False


        # ADD USER
        elif command.code == '!user_create':

            try:
                # Creating New User
                username = self.format_username(content.split(' ')[1])
                discord_id = content.split(' ')[2]
                message, success, data = self.create_user(db_access, discord_id, username, command)
            except Exception as e: 
                message = self.warning(command, f'Error creating user: *{e}*')
                success = False


        # DELETE USER
        elif command.code == '!user_delete':

            try: 
                # Removing User
                username = content.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = self.warning(command, f'User [{username}] does not exist')
                    success = False
                else:
                    db_access.group_resource.remove_user(user)
                    message = self.warning(command, f'User [{username}] deleted successfully')
            except Exception as e: 
                message = self.warning(command, f'Error deleting user: *{e}*')
                success = False


        # FREEZE USER
        elif command.code == '!user_freeze':

            try:  
                username = content.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = self.warning(command, f'User [{username}] does not exist')
                    success = False
                else:
                    user.frozen = True
                    db_access.group_resource.update_user(user)
                    message = self.warning(command, f'Freezing user: [{username}]')
            except Exception as e:
                message = self.warning(command, f'Error freezing user: *{e}*')
                success = False


        # UNFREEZE USER
        elif command.code == '!user_unfreeze':

            try:  
                username = content.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                if user is None:
                    message = self.warning(command, f'User [{username}] does not exist')
                    success = False
                else:
                    user.frozen = False
                    db_access.group_resource.update_user(user)
                    message = self.warning(command, f'Unfreezing user: [{username}]')
            except Exception as e:
                message = self.warning(command, f'Error unfreezing user: *{e}*')
                success = False

        # USER INFO
        elif command.code == '!user_info':

            try: 
                username = content.split(' ')[1]
                user = db_access.group_resource.get_user_by_username(username, self.group_id)
                user_contributions = db_access.session_resource.get_user_contributions(user.discord_id, self.group_id)

                if user is None:
                    message = self.warning(command, f'User [{username}] does not exist')
                    success = False
                else:
                    badges = db_access.group_resource.get_user_badges(user.id)
                    _badges = '\n'.join([f'  - {b.emoji} {b.name} - *{b.description}*' for b in badges])

                    message = self.title(command, f'User Info: {user.name}')
                    message = message + f'- **Current Streak**: {user.streak}' + \
                        f'\n- **Best Streak**: {user.best_streak}' + \
                        f'\n- **Points**: {user.points}' + \
                        f'\n- **Frozen**: {user.frozen}' + \
                        f'\n- **Contributions**: {len(user_contributions)}' + \
                        f'\n- **Last Participation**: {user.last_participation}' + \
                        f'\n- **Badges**:' + \
                        (_badges if badges else '  - No badges yet')
                    
                        
            except Exception as e:
                message = self.warning(command, f'Error getting user info: *{e}*')
                success = False 


        # USER LIST
        elif command.code == '!user_list':

            try: 
                users: list[User] = db_access.group_resource.get_group_users(self.group_id)
                message = self.title(command, 'Users in group')
                users_list = '\n'.join([
                    f'`{self.padding_space(u.name, 20)}` - streak: {u.streak} - points: {u.points} - frozen: {u.frozen}' 
                    for u in users if u.active])
                message = message + users_list
            except Exception as e:
                message = self.warning(command, f'Error listing users: *{e}*')
                success = False


        # USER POINTS
        elif command.code == '!points':

            try: 
                users: list[User] = db_access.group_resource.get_group_users(self.group_id)
                message = self.title(command, 'User points')
                users_points = '\n'.join([f'- **{u.name}** - {u.points}' for u in users])
                message = message + users_points
            except Exception as e:
                message = self.warning(command, f'Error listing points: *{e}*')
                success = False


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
                success = False

        # LIST SCHEDULES
        elif command.code == '!schedule_list':

            try: 
                message = self.title(command, 'Available schedules')
                schedules = '\n'.join([f'* **{s.id}** --- {s.name} --- *{s.description}*' for s in SCHEDULES])
                message = message + schedules
            except Exception as e:
                message = self.warning(command, f'Error listing schedules *{e}*')
                success = False

        
        # SET SCHEDULE
        elif command.code == '!schedule_set':

            try: 
                schedule_id = content.split(' ')[1]
                available_ids = [s.id for s in SCHEDULES]
                if schedule_id not in available_ids:
                    message = self.warning(command, f'Schedule [{schedule_id}] does not exist')
                    success = False
                else: 
                    group: Group = db_access.group_resource.get_group(self.group_id)
                    group.schedule_id = schedule_id
                    db_access.group_resource.modify_schedule(group, schedule_id)

                    message = self.warning(command, f'Schedule [{schedule_id}] set successfully')
            except Exception as e:
                message = self.warning(command, f'Error setting schedule: *{e}*')
                success = False


        # START
        elif command.code == '!start':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                group.is_active = True
                db_access.group_resource.update_group(group)
                message = self.warning(command, 'The group is reactivated, sessions are active.')
            except Exception as e:
                message = self.warning(command, f'Error reactivating group *{e}*')
                success = False

        # PAUSE
        elif command.code == '!pause':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                group.is_active = False
                db_access.group_resource.update_group(group)
                message = self.warning(command, 'The group is paused, sessions are inactive.')
            except Exception as e:
                message = self.warning(command, f'Error pausing group *{e}*')
                success = False


        # SETTINGS
        elif command.code == '!settings_show':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                message = settings.show_settings()
            except Exception as e:
                message = self.warning(command, f'Error showing settings: *{e}*')
                success = False
                print(traceback.format_exc())
 


        # SETTINGS INC
        elif command.code == '!settings_incognito':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                new_settings = dataclasses.replace(settings, incognito=bool(int(content.split(' ')[1], 0)))
                group.settings = json.dumps(new_settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Incognito mode set to {new_settings.incognito}')
            except Exception as e:
                message = self.warning(command, f'Error toggling incognito mode *{e}*')
                success = False

        
        # SETTINGS GER
        elif command.code == '!settings_ger':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                new_settings = dataclasses.replace(settings, genre_explo_ratio=float(content.split(' ')[1], 0.5))
                group.settings = json.dumps(new_settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Genre Exploration Ratio set to {new_settings.genre_explo_ratio}')
            except:
                message = self.warning(command, 'Error setting genre exploration ratio')
                success = False


        # SETTNGS GSR
        elif command.code == '!settings_gsr':

            try: 
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                new_settings = dataclasses.replace(settings, genre_subgenre_ratio=float(content.split(' ')[1], 0.5))
                group.settings = json.dumps(new_settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Genre / Subgenre Ratio set to {new_settings.genre_subgenre_ratio}')
            except:
                message = self.warning(command, 'Error setting genre/subgenre ratio')
                success = False


        # SETTINGS GPR
        elif command.code == '!settings_gpr':

            try: 
                args=content.split(' ')
                group: Group = db_access.group_resource.get_group(self.group_id)
                settings: Settings = Settings.from_dict(json.loads(group.settings))
                genre, weight = GenreName(args[1]), int(args[2])
                new_settings = dataclasses.replace(settings, genre_weights={**settings.genre_weights, genre: weight})
                group.settings = json.dumps(settings.to_dict())
                db_access.group_resource.update_group(group)
                message = self.warning(command, f'Genre Proportion for {genre.name} set to {weight}')
            except Exception as e:
                message = self.warning(command, f'Error setting genre proportion: *{e}*')
                success = False
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
                success = False


        return message, success, data

    
    # Helper Function to create user
    def create_user(self, db_access: DatabaseAccess, discord_id: int, username: str, command: Command) -> tuple[str, dict[str, Any]]: 

        success, data = True, {}
        group_users: list[User] = db_access.group_resource.get_group_users(self.group_id)

        if any([u.discord_id == discord_id for u in group_users]):

            # Renaming User
            user = [u for u in group_users if u.discord_id == discord_id][0]
            user.name = username
            db_access.group_resource.update_user(user)

            message = self.warning(command, f'User with discord ID [{discord_id}] already exists, renaming to [{username}]')
            success = False

        elif any([u.name == username for u in group_users]):

            message = self.warning(command, f'User with name [{username}] already exists')
            success = False

        elif username == '' or username is None:

            message = self.warning(command, f'Invalid username')
            success = False

        else: 
            # Adding New User 
            new_user = User(
                discord_id=discord_id,
                group_id=self.group_id,
                name=username
            )
            db_access.group_resource.add_user(new_user)

            message = self.warning(command, f'User {new_user.name} created successfully')
            data = {'new_user': new_user}

        return message, success, data


    
    @staticmethod
    def check_commands(messages: list[discord.Message]) -> list[tuple[Command, discord.Message]]:

        commands = []
        for message in reversed(messages):
            for command in COMMANDS:
                if command.code in message.content and not message.author.bot:
                    commands.append((command, message))

        print(f'[LOG] -- Found {len(commands)} commands')
    
        return commands
    
    @staticmethod
    def block_command(command: Command, user: User) -> tuple[str, bool]:

        # Restricted Command  
        if command.restricted and user is not None and not user.admin:

            text = 'You do not have permission to use this command'
            message = CommandCenter.warning(command, text)
            return message, True
        
        elif command.name not in ['ME'] and user is None:

            text = 'User need to be registered to use this command'
            message = CommandCenter.warning(command, text)
            return message, False
        
        return '', False
        
    @staticmethod
    def title(command: Command, message: str) -> str:
        return f'**[{command.name}]** -- **{message}**\n'
    
    @staticmethod
    def warning(command: Command, message: str) -> str:
        return f'**[{command.name}]** - {message}'
    
    @staticmethod   
    def padding_space(message: str, max_space: int) -> str:
        message_length = len(message)
        padding = max_space - message_length
        return  message + ' ' * padding
    
    @staticmethod
    def format_username(username: str) -> str:
        
        MAX_USERNAME_LENGTH = 30
        username = ''.join(c for c in username if c.isalnum() or c == '-')[:MAX_USERNAME_LENGTH]

        return username


