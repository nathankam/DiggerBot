"""
import datetime
import pickle
from typing import Any
from fbchat import Client
from fbchat.models import *
from dotenv import load_dotenv
import os

from src.data.commands import COMMANDS
from src.models.message import Command
from src.services.commands import CommandCenter

# Create the bot client
class MessengerBot(Client):

    def send_message(self, message, group_id):
        
        self.send(
            Message(text=message), 
            thread_id=group_id, 
            thread_type=ThreadType.GROUP
        )

    def check_commands(self, group_id, bot_refresh_rate: int, limit=100) -> list[dict]:

        # Fetch last 'limit' messages from the group
        messages = self.fetchThreadMessages(thread_id=group_id, limit=limit)
        messages.reverse()

        # Check for commands in each message
        commands = []
        for message in messages:
            now = datetime.now()
            delta_bot = datetime.timedelta(seconds=bot_refresh_rate)
            in_timeframe = message.timestamp >= now - delta_bot
            for command in COMMANDS:
                if command.code in message.text and in_timeframe:
                    commands.append({
                        'command': command, 
                        'message': message
                    })

        return commands
            

    def get_group_messages(self, group_id, search_string='', limit=100):

        # Fetch last 'limit' messages from the group
        messages = self.fetchThreadMessages(thread_id=group_id, limit=limit)
        messages.reverse()  # Oldest first
        matching_messages = []

        # Search for the string in each message
        for message in messages:
            if search_string.lower() in message.text.lower() or search_string=='':  # Case-insensitive search
                matching_messages.append(message)

        return matching_messages
    

    def get_group_messages_within_timeframe(self, group_id, start_time, end_time, search_string='', limit=100):

        # Fetch last 'limit' messages from the group
        messages = self.fetchThreadMessages(thread_id=group_id, limit=limit)
        messages.reverse()

        matching_messages = []

        # Search for the string in each message
        for message in messages:
            if search_string.lower() in message.text.lower() or search_string=='':
                if start_time <= message.timestamp <= end_time:
                    matching_messages.append(message)

        return matching_messages
    

    def get_message_reacts(self, group_id, message_id) -> list[dict]:

        # Fetch message details by ID
        message = self.fetchMessageInfo(message_id, thread_id=group_id)
        
        # Extract reactions (if any)
        if message and message_id in message:
            message_data = message[message_id]
            reacts = message_data.reactions
            return reacts
        
        return None
"""