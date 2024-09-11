import datetime
from typing import Optional
import discord


from src.data.commands import COMMANDS
from src.persistence.models.group import Group

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


    async def get_last_messages(self, channel_id: int, last_check: datetime.datetime, limit=100):

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
            print(f' -> [ERR] ---  Error fetching messages: {e}')

    async def get_message_reactions(self, channel_id: int, message_id: int) -> Optional[list[discord.Reaction]]:

        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel:
            return None

        message: discord.Message = await channel.fetch_message(message_id)
        if message:
            return message.reactions
    
        return None
    