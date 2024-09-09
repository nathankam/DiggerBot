import datetime
import json
from fbchat import Client
from fbchat.models import *
from dotenv import load_dotenv
import os
import schedule
import time

from data.schedules import SCHEDULES
from models.message import Command
from models.music import Theme
from models.schedule import Event
from persistence.models.contribution import Contribution
from persistence.models.session import Session
from persistence.models.group import Group
from persistence.models.user import User
from services.commands import CommandCenter
from services.messenger import MessengerBot
from services.helpers import count_votes, detect_contributions, get_session_number, pick_theme
from services.gamemaster import GameMaster

from src.persistence.database import DatabaseAccess

# Load credentials from .env file
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BOT_REFRESH_RATE = os.getenv("BOT_REFRESH_RATE")

# Create a database connection
database = DatabaseAccess(os.getenv("DB_URI"))


def check_chats(): 

    bot = MessengerBot(EMAIL, PASSWORD)

    groups: list[Group] = database.group_resource.get_groups()

    if not groups: 
        print("No active groups found") 
        return

    # Check for each group
    for group in groups:

        # Check for commands
        commands: list[dict] = bot.check_commands(group.id, BOT_REFRESH_RATE)
        commandCenter = CommandCenter(bot, group.id)
        for command_dict in commands: 
            command: Command = command_dict['command']
            message: Message = command_dict['message']
            commandCenter.execute(message.text, message.uid, command, database)

        # Get session and schedule
        session = database.session_resource.get_active_sessions(group.id)
        schedule = [s for s in SCHEDULES if s.id == group.schedule_id][0]
        
        # There is an ongoing session
        if session is not None:

            # Get the ongoing session
            ongoing_session: Session = session[0]

            # Vote Event
            if detected_event == 'Vote':

                # Detect Contributions
                contributions: list[Contribution] = detect_contributions(group.id)
                database.session_resource.create_contributions(contributions)

                # No Contributions - Kill Bot
                if not contributions:
                    last_session_number = database.session_resource.get_last_active_session_number(group.id)
                    participation_timeout = 3 - (ongoing_session.session_number - last_session_number)
                    if participation_timeout > 0:
                        GameMaster.no_contributions(participation_timeout)
                    else:
                        group.is_active = False    
                        database.group_resource.update_group(group)
                        GameMaster.killing_bot()
                        
                    continue

                # User Streak Update
                streaks = {}
                for contribution in contributions:
                    user: User = database.group_resource.get_user_by_id(contribution.user_id, group.id)
                    user.streak = user.streak + 1 if user.last_participation == ongoing_session.session_number - 1 else 1
                    user.last_participation = ongoing_session.session_number
                    streaks[user.name] = user.streak
                    database.group_resource.update_user(user)

                # Close Participation
                gameMaster = GameMaster(bot, theme, group.id)
                gameMaster.close_participation(contributions, streaks)
                
            # End Event
            elif detected_event == 'End':

                # Get Contributions
                contributions: list[Contribution] = database.session_resource.get_contributions(ongoing_session.id)
                votes, reacts, winners, points, is_banger = count_votes(contributions)

                # Update Contributions 
                for contribution in contributions:

                    # Contribution Update
                    contribution.reacts = reacts[contribution.user_id]
                    contribution.points = points[contribution.user_id]
                    if contribution.user_id in winners: 
                        contribution.winner = True
                        contribution.banger = is_banger
                    database.session_resource.update_contribution(contribution)

                    # Points Update
                    user: User = database.group_resource.get_user_by_id(contribution.user_id, group.id)
                    user.points = user.points + contribution.points

                # Close Votes
                gameMaster = GameMaster(bot, theme, group.id)
                gameMaster.close_votes(votes, winners)

                # Close Session 
                database.session_resource.set_session_inactive(ongoing_session)

        # No sesssion ongoing - Only start a session when there is no ongoing session
        elif group.is_active: 

            # Check the events for today
            now = datetime.datetime.now()
            detected_event = schedule.check_events(now)

            if detected_event == 'Start':

                scheduled_events = schedule.get_events_dates(now)
                if scheduled_events is None: print("Error in events scheduling")

                theme: Theme = pick_theme(group.settings)
        
                session = Session(
                    group_id=group.id,
                    schedule_id=group.schedule_id,
                    session_number=database.session_resource.get_last_session_number(group.id) + 1,
                    theme = json.dumps(theme),
                    start_at=datetime.datetime.now(),
                    vote_at=scheduled_events['vote'],
                    end_at=scheduled_events['end']
                )

                database.session_resource.create_session(session)

                # New GameMaster
                gameMaster = GameMaster(bot, theme, group.id)
                gameMaster.start()


def session():

    bot = MessengerBot(EMAIL, PASSWORD)

    session = Session(theme=pick_theme(), session_number=get_session_number())

    session.start()
    schedule.every().day.at(session.vote_time.strftime("%H:%M")).do(session.close_participations)
    schedule.every().day.at(session.end_time.strftime("%H:%M")).do(session.close_votes)


# Schedule the message to send every day at a specific time
schedule.every().day.at("09:00").do(session)


while True:
    schedule.run_pending()
    time.sleep(BOT_REFRESH_RATE)