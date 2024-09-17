import datetime
from typing import Optional
import discord


from src.data.commands import COMMANDS
from src.persistence.models.group import Group
from src.persistence.models.user import User

class DiscordBot(discord.Client):

    def __init__(self):

        # Intents 
        intents = discord.Intents.default()
        intents.messages = True
        intents.reactions = True
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        super().__init__(intents=intents)


    async def send_message(self, message: str, channel_id: int):

        # Get Channel And Send Message
        channel = self.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print("Channel not found")


    async def get_last_messages(self, channel_id: int, last_check: datetime.datetime, limit=100) -> list[discord.Message]:

        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel:
            return []
        
        print(f'[LOG] --- Checking {channel_id} ({channel})', end='')

        # Filter Messages
        try: 
            matching_messages = []
            messages = channel.history(limit=limit)
            messages = [msg async for msg in messages]

            for msg in messages:
                if msg.created_at >= last_check: matching_messages.append(msg)
            print(f' -> {len(matching_messages)} new messages')
            return matching_messages
        
        except Exception as e: 
            print(f' -> Error fetching messages: {e}')


    async def get_users_pm(self, users: list[User], last_check: datetime.datetime) -> dict[int, list[discord.Message]]:

        # Go look for user dms
        users_pm_dict = {}
        for user in users:
            user_dms = await self.get_last_messages(user.dm_channel_id, last_check)

            # Filter out messages that are replies to other group concerns 
            for dm in user_dms:
                if dm.reference:
                    parent = await dm.channel.fetch_message(dm.reference.message_id)
                    if user.group_id not in parent.content: user_dms.remove(dm)

            users_pm_dict[user.id] = user_dms

        return users_pm_dict
    

    async def get_pmessages(self, users: list[User], last_check: datetime.datetime) -> list[discord.Message]:

        # Go look for user dms
        pmessages = []
        for user in users:

            print(f'[LOG] --- Checking {user.name} dms ', end='') 

            if user.dm_channel_id is None: 
                print(f'-> dm channel not found')
                continue

            user_dms = await self.get_last_messages(user.dm_channel_id, last_check)

            # Filter out messages that are replies to other group concerns 
            for dm in user_dms:
                if dm.reference:
                    parent = await dm.channel.fetch_message(dm.reference.message_id)
                    if user.group_id not in parent.content: user_dms.remove(dm)

            pmessages.extend(user_dms)

            print(f'-> {len(user_dms)} new messages ({user.dm_channel_id})')

        return pmessages


    async def get_message_reactions(self, channel_id: int, message_id: int) -> Optional[list[discord.Reaction]]:

        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel:
            return None

        message: discord.Message = await channel.fetch_message(message_id)
        if message:
            return message.reactions
    
        return None
    