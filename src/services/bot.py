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


    async def send_message(self, message: str, channel_id: int) -> int:

        # Get Channel And Send Message
        channel = self.get_channel(channel_id)
        if channel:
            message: discord.Message = await channel.send(message)
            return message.id
        else:
            print(f"[ERR] - Channel {channel_id} not found")
            return None
            

    async def send_pm(self, message: str, discord_id: int):

        # Get User
        user = self.get_user(discord_id)
        if user:
            await user.send(message)
        else:
            print(f"[ERR] - User {discord_id} not found")


    async def get_last_messages(self, channel_id: int, last_check: datetime.datetime, limit=100) -> list[discord.Message]:

        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel: return []
        
        print(f'[LOG] -- Checking {channel_id} ({channel})', end='')

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


    async def get_last_pmessages(self, user: User, last_check: datetime.datetime) -> list[discord.Message]:

        # Fetch the user by their Discord ID
        discord_user = await self.fetch_user(user.discord_id)

        # Create or fetch the DM channel
        dm_channel = await discord_user.create_dm()

        # Fetch the message history
        messages = dm_channel.history(limit=100)
        messages = [msg async for msg in messages if msg.created_at >= last_check]

        return messages
    

    async def get_pmessages(self, users: list[User], last_check: datetime.datetime) -> list[discord.Message]:

        # Go look for user dms
        pmessages = []
        for user in users:

            print(f'[LOG] --- Checking {user.name} dms ', end='') 

            user_dms = await self.get_last_pmessages(user, last_check)
            print(f'[TEST-LOG]  --> {len(user_dms)} new messages')

            # Filter out messages that are replies to other group concerns 
            for dm in user_dms:
                if dm.reference:
                    parent = await dm.channel.fetch_message(dm.reference.message_id)
                    if f'G{user.group_id}' not in parent.content: user_dms.remove(dm)

            pmessages.extend(user_dms)

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
    