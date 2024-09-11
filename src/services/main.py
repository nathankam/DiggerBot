import argparse
import traceback
import datetime
import json
from typing import Optional
from dotenv import load_dotenv
import os, sys, asyncio
import discord
import pytz

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.schedules import SCHEDULES
from src.models.music import Theme
from src.models.settings import Settings

from src.persistence.database import DatabaseAccess
from src.persistence.models.contribution import Contribution
from src.persistence.models.session import Session
from src.persistence.models.group import Group
from src.persistence.models.user import User

from src.services.commands import CommandCenter
from src.services.bot import DiscordBot
from src.services.helpers import count_votes, detect_contributions, pick_theme
from src.services.gamemaster import GameMaster

# TEST VARIABLES
TEST=None
TEST_DATE_UTC=datetime.datetime(2000, 1, 1, 8, 3, 0, 0, pytz.UTC)

# Load credentials from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_URL = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

# Discord Bot / Database
bot = DiscordBot()
database = DatabaseAccess(os.environ['DATABASE_URL'])

async def check_chats(): 

    # Get all the groups
    groups: list[Group] = database.group_resource.get_groups()
    if not groups: 
        return

    # Check for each group
    for group in groups:

        # Log 
        print(f"[LOG] -- Parsing group {group.name}")
        error_message = ''

        # Get last messages
        try: 
            messages: list[discord.Message] = await bot.get_last_messages(group.channel_id, group.last_check)
            group.last_check = datetime.datetime.now(pytz.UTC)
            database.group_resource.update_group(group)
        except Exception as e:
            error_message += f"[BOT] / Message extraction failed **{e}**\n"
            continue
        
        # Check for commands 
        commands = CommandCenter.check_commands(messages)
        commandCenter = CommandCenter(bot, group.id)
        for (command, msg) in commands: 
            info = commandCenter.execute(msg.content, msg.author.id, command, database)
            await bot.send_message(message=info, channel_id=group.channel_id)

        # Get session and schedule
        session: Optional[Session] = database.session_resource.get_active_session(group.channel_id)
        schedule = [s for s in SCHEDULES if s.id == group.schedule_id][0]

        # Check the next event
        now_utc = datetime.datetime.now(pytz.UTC) if not TEST else TEST_DATE_UTC
        detected_event = schedule.check_events(now_utc, group.timezone)

        print(f'[LOG] -- Detected Event: {detected_event}')
    
        # No sesssion ongoing - Only start a session when there is no ongoing session
        if session is None and group.is_active: 

            print(f'[LOG] -- No Ongoing Session')

            if detected_event == 'Start' or TEST=='START':

                print(f'[LOG] -- Detected Start Event')
                try: 

                    # Get the next scheduled vents
                    scheduled_events = schedule.get_events_dates(now_utc, group.timezone)
                    if scheduled_events is None: print("Error in next events scheduling")

                    # Theme Choice
                    group_settings = Settings.from_dict(json.loads(group.settings))
                    theme = pick_theme(group_settings)

                    # Session Making 
                    session = Session(
                        channel_id=group.channel_id,
                        schedule_id=group.schedule_id,
                        session_number=database.session_resource.get_last_session_number(group.channel_id) + 1,
                        theme = json.dumps(theme.to_dict()),
                        start_at=now_utc, 
                        vote_at=scheduled_events['vote'], 
                        end_at=scheduled_events['end'],
                        incognito=group_settings.incognito
                    )
                    database.session_resource.create_session(session)

                    # New GameMaster
                    gameMaster = GameMaster(session)
                    await bot.send_message(
                        message=gameMaster.start(theme, group.timezone),
                        channel_id=group.channel_id
                    )

                except Exception as e:
                    error_message += f"[BOT] / Start Event failed **{e}**\n"
                    print(f"[ERR] -- Session creation failed: {e}")


        # There is an ongoing session
        elif session is not None:

            print(f'[LOG] -- Ongoing Session: {session}')

            # Vote Event
            if detected_event == 'Vote' or TEST=='VOTE':

                print(f'[LOG] -- Detected Vote Event')
                try: 

                    # Detect Contributions
                    users = database.group_resource.get_group_users(group.id)
                    contributions: list[Contribution] = detect_contributions(messages, session, users)
                    if len(contributions) > 0: database.session_resource.create_contributions(contributions)

                    # No Contributions - Kill Bot
                    if len(contributions) == 0:

                        print(f'[LOG] -- No Contributions Detected')

                        # Participation Timeout
                        last_session_number = database.session_resource.get_last_active_session_number(group.channel_id)
                        participation_timeout = 3 - (session.session_number - last_session_number)
                        
                        if participation_timeout > 0:

                            # Close Session
                            database.session_resource.set_session_inactive(session)
                            await bot.send_message(
                                message=GameMaster.no_contributions(participation_timeout),
                                channel_id=group.channel_id
                            )

                        else:

                            # Close Session - Kill Bot 
                            group.is_active = False    
                            database.session_resource.set_session_inactive(session)
                            database.group_resource.update_group(group)
                            await bot.send_message(
                                message=GameMaster.killing_bot(),
                                channel_id=group.channel_id
                            )

                    # Contributions Detected
                    else:

                        print(f'[LOG] -- Contributions Detected: {len(contributions)}')

                        # User Streak Update
                        streaks = {}
                        for contribution in contributions:
                            user: User = database.group_resource.get_user_by_id(contribution.user_id, group.id)
                            print(f'[LOG] -- User {user}')
                            if user is not None:
                                user.streak = user.streak + 1 if user.last_participation == session.session_number - 1 else 1
                                user.last_participation = session.session_number
                                streaks[user.name] = user.streak
                                database.group_resource.update_user(user)
                            else:
                                print(f"[ERR] -- User {contribution.user_id} not found")

                        # Close Participation
                        gameMaster = GameMaster(session=session)
                        await bot.send_message(
                            message=gameMaster.close_participation(contributions, streaks, group.timezone),
                            channel_id=group.channel_id
                        )

                except Exception as e:
                    error_message += f"[BOT] / Vote Event failed **{e}**\n"
                    print(f"[ERR] -- Vote Event failed: {e}")
                    
            # End Event
            elif detected_event=='End' or TEST=='END':
                    
                try: 

                    print(f'[LOG] -- Detected End Event')

                    # Get Contributions   
                    contributions: list[Contribution] = database.session_resource.get_contributions(session.id)
                    votes, reacts, winners, points, is_banger = await count_votes(bot, session, contributions)

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
                    gameMaster = GameMaster(session=session)
                    await bot.send_message(
                        message=gameMaster.close_votes(votes, winners),
                        channel_id=group.channel_id
                    )

                    # Close Session 
                    database.session_resource.set_session_inactive(session)

                except Exception as e:
                    error_message += f"[BOT] / End Event failed **{e}**\n"
                    print(f"[ERR] -- End Event failed: {e}")

            else: 

                print(f'[LOG] -- No Event Detected, nothing to do')

        
        # Error Message
        if error_message != '': await bot.send_message(error_message, group.channel_id)

            

@bot.event
async def on_ready():

    print(f'[BOT START] - {bot.user} has connected to Discord!')
    await check_chats()
    await bot.close()
    print(f'[BOT CLOSE] - Disconnecting {bot.user} from Discord!')
    

if __name__ == '__main__':

    asyncio.run(bot.start(TOKEN))
