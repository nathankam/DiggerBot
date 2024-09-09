import datetime
from typing import Optional
import discord

from src.data.commands import COMMANDS

from discord import Message


class DiscordBot(discord.Client):

    def __init__(self, token: str):

        super().__init__()
        self.token = token


    async def send_message(self, message: str, channel_id: int):

        # Get Channel And Send Message
        channel = self.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            print("Channel not found")


    async def check_commands(self, channel_id: int, bot_refresh_rate: int, limit=100) -> list[dict]:
        
        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel:
            return []

        now = datetime.utcnow()
        delta_bot = datetime.timedelta(seconds=bot_refresh_rate)
        messages: list[Message] = await channel.history(limit=limit).flatten()
        commands = []

        for message in reversed(messages):
            if message.created_at >= now - delta_bot:
                for command in COMMANDS:
                    if command.code in message.content:
                        commands.append({
                            'command': command,
                            'message': message
                        })
        
        return commands
    
    
    async def get_channel_messages(self, channel_id: int, search_string='', limit=100):

        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel:
            return []

        messages: list[Message] = await channel.history(limit=limit).flatten()
        matching_messages = [msg for msg in messages if search_string.lower() in msg.content.lower()]
        
        return matching_messages


    async def get_messages_within_timeframe(self, channel_id: int, start_time: datetime, end_time: datetime, search_string='', limit=100):

        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel:
            return []

        messages: list[Message] = await channel.history(limit=limit).flatten()
        matching_messages = [
            msg for msg in messages
            if start_time <= msg.created_at <= end_time and search_string.lower() in msg.content.lower()
        ]
        
        return matching_messages
    

    async def get_message_reactions(self, channel_id: int, message_id: int) -> Optional[list[discord.Reaction]]:

        # Get Channel
        channel = self.get_channel(channel_id)
        if not channel:
            return None

        message: Message = await channel.fetch_message(message_id)
        if message:
            return message.reactions
    
        return None
    