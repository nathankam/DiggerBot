import traceback
import datetime
import json
from typing import Optional
from dotenv import load_dotenv

import os, sys, asyncio
import discord
import pytz


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.models.badge import Badge
from src.persistence.models.badge import UserBadge
from src.services.badger import Badger

from src.data.schedules import SCHEDULES
from src.models.music import Theme
from src.models.settings import Settings

from src.persistence.database import DatabaseAccess
from src.persistence.models.contribution import Contribution
from src.persistence.models.session import Session
from src.persistence.models.group import Group
from src.persistence.models.user import User

from src.services.recommander import Recommander
from src.services.commands import CommandCenter
from src.services.bot import DiscordBot
from src.services.gamemaster import GameMaster
from src.services.helpers import (
    badge_update, compute_streak, detect_contributions, extract_link, 
    kill_session, pick_theme, vote_analysis, welcome_user
)

# TEST VARIABLES
TEST = ''
TEST_DATE_UTC = datetime.datetime(2000, 1, 1, 22, 3, 0, 0, pytz.UTC)
TEST_GROUP = 'DiggerBotTest'
# -> Switch TEST_DATE_UTC to START/VOTE/END to force events or DATE to test a specific date
# -> Synchronize the TEST_DATE with an event in the schedule (1 jour before to account for timzeone)

# VARIABLES
MIN_USERS = 1

# Load credentials from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_URL = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

# Discord Bot / Database
bot = DiscordBot()
database = DatabaseAccess(DATABASE_URL)

async def check_chats(): 

    # Get all the groups
    groups: list[Group] = database.group_resource.get_groups()

    # Check for new groups
    group_ids = [group.channel_id for group in groups]
    for guild in bot.guilds:

        # Guild Text Channels
        general_channel = next((channel for channel in guild.text_channels if channel.name == 'general'), None)
        if general_channel is None or general_channel.id in group_ids: 
            continue # No General Channel / Already in the database

        # Create Groupe
        group = Group(channel_id=general_channel.id, name=guild.name) 
        groups.append(group)
        database.group_resource.create_group(group)

        await bot.send_message(
            message=GameMaster.welcome(group.language),
            channel_id=group.channel_id
        )

    # Check for each group
    for group in list(set(groups))  :

        # Log 
        print(f"\n[GROUP] - [{group.name}]")
        error_message = ''

        # Get last messages
        messages: list[discord.Message] = await bot.get_last_messages(group.channel_id, group.last_check)
        group.last_check = datetime.datetime.now(pytz.UTC)
        database.group_resource.update_group(group)
        
        # Check for commands 
        commands = CommandCenter.check_commands(messages)
        commandCenter = CommandCenter(bot, group.id)
        for (command, msg) in commands: 
            info, success, data = commandCenter.execute(msg.content, msg.author.id, command, database)
            await bot.send_message(message=info, channel_id=group.channel_id)
            if command.code in ['!user_create', '!me'] and success: 
                await welcome_user(data['new_user'], group, bot, database)

        # Get current time 
        now_utc = datetime.datetime.now(pytz.UTC)
        now_utc = TEST_DATE_UTC if TEST and TEST_GROUP == group.name else now_utc

        # Get session and schedule
        session: Optional[Session] = database.session_resource.get_active_session(group.channel_id)
        schedule = [s for s in SCHEDULES if s.id == group.schedule_id][0]
        detected_event = schedule.check_events(now_utc, group.timezone)

        print(f'[LOG] -- Detected Event: {detected_event}')
    
        # No sesssion ongoing - Only start a session when there is no ongoing session
        if session is None and group.is_active: 

            print(f'[LOG] -- No Ongoing Session')

            if detected_event == 'Start' or (TEST=='START' and group.name == TEST_GROUP):

                try: 
                    # Check if enough users
                    users: list[User] = database.group_resource.get_group_users(group.id)
                    if len(users) < MIN_USERS:
                        await bot.send_message(
                            message=GameMaster.not_enough_users(users, group, MIN_USERS),
                            channel_id=group.channel_id
                        )
                        continue

                    # Get the next scheduled vents
                    scheduled_events = schedule.get_events_dates(now_utc, group.timezone)
                    if scheduled_events is None: print("Error in next events scheduling")

                    # Theme Choice
                    group_settings: Settings = Settings.from_dict(json.loads(group.settings))
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

                    # Start Event
                    await bot.send_message(
                        message=GameMaster.start(theme, group, session),
                        channel_id=group.channel_id
                    )

                    # Send DMs if incognito session
                    for user in users if session.incognito else []:
                        if user.dm_channel_id is None: continue
                        await bot.send_pm(
                            message=GameMaster.start_dm(theme, group, session),
                            discord_id=user.discord_id
                        )

                except Exception as e:
                    error_message += f"[BOT] / Start Event failed **{e}**\n"
                    print(f"[ERR] -- Session creation failed: {e}")


        # There is an ongoing session
        elif session is not None:

            print(f'[LOG] -- Ongoing Session: {session}')

            # DM Parsing if Incognito Mode
            participation_open = session.start_at < now_utc < session.vote_at
            if session.incognito and participation_open:
                # Detect Anonymous Contributions
                pmessages = await bot.get_pmessages(users, group.last_check)
                anonymous_contributions = detect_contributions(pmessages, session, users)
                if not anonymous_contributions: return 

                # Announce Anonymous Contributions
                ms = GameMaster.anonymous_contributions(anonymous_contributions)
                for (idx, m) in enumerate(ms) if ms is not None else []:
                    message_id = await bot.send_message(message=m, channel_id=group.channel_id)
                    anonymous_contributions[idx].message_id = message_id
                database.session_resource.create_contributions(anonymous_contributions)

            # Vote Event
            if detected_event == 'Vote' or (TEST=='VOTE' and group.name == TEST_GROUP):

                try: 
                    # Detect Contributions
                    users: list[User] = database.group_resource.get_group_users(group.id)
                    messages = await bot.get_last_messages(group.channel_id, session.start_at)
                    contributions: list[Contribution] = detect_contributions(messages, session, users)

                    # Anonymous Contributions
                    if session.incognito:
                        contributions_incognito: list[Contribution] = database.session_resource.get_contributions(session.id)
                        contributions += contributions_incognito

                    # No Contributions - Kill Bot
                    if len(contributions) == 0:

                        print(f'[LOG] -- No Contributions Detected')
                        await kill_session(bot, session, group, database)

                    # Contributions Detected
                    else:
                        print(f'[LOG] -- Contributions Detected: {len(contributions)}')

                        # Contributions
                        database.session_resource.create_contributions(contributions)
                        database.group_resource.streak_increment(group)

                        # User Streak Update
                        streaks = {}
                        for contribution in contributions:
                            user: User = database.group_resource.get_user_by_id(contribution.user_discord_id, group.id)
                            user, streak = compute_streak(user, session)
                            streaks[user.name] = streak
                            database.group_resource.update_user(user)

                        # Spotify Recommandation
                        spotilinks = [extract_link(c.content) for c in contributions if c.platform == 'SPOTIFY']
                        if len(spotilinks) > 0:
                            recommander = Recommander(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
                            reco = recommander.get_recommandation(spotilinks, limit=1)

                            await bot.send_message(
                                message=GameMaster.recommandation(reco[0]),
                                channel_id=group.channel_id
                            )

                        # Close Participation
                        await bot.send_message(
                            message=GameMaster.close_participation(session, contributions, streaks, group),
                            channel_id=group.channel_id
                        )

                except Exception as e:
                    error_message += f"[BOT] / Vote Event failed **{e}**\n"
                    
            # End Event
            elif detected_event=='End' or (TEST=='END' and group.name == TEST_GROUP):
                    
                try: 
                    # Get Contributions   
                    users: list[User] = database.group_resource.get_group_users(group.id)
                    contributions: list[Contribution] = database.session_resource.get_contributions(session.id)
                    votes, winners = await vote_analysis(bot, session, group, database, contributions)

                    # Close Votes
                    await bot.send_message(
                        message=GameMaster.close_votes(session, group, users, votes, winners),
                        channel_id=group.channel_id
                    )

                    # Close Session 
                    database.session_resource.set_session_inactive(session)
                    await badge_update(users, group, database)

                except Exception as e:
                    error_message += f"[BOT] / End Event failed **{e}**\n"
                    print(f"[ERR] -- End Event failed: {e}")
                    print(traceback.format_exc())

            else: 

                if detected_event != 'Start': 
                    print(f'[LOG] -- No Event Detected, nothing to do')

        
        # Error Message
        if error_message != '': await bot.send_message(error_message, group.channel_id)

            

@bot.event
async def on_ready():

    try: 
        print(f'[BOT START] - {bot.user} has connected to Discord!')
        await check_chats()
    except Exception as e:
        print(f'[BOT ERROR] - {e}')
        print(traceback.format_exc())
    finally: 
        await bot.close()
        print(f'[BOT CLOSE] - Disconnecting {bot.user} from Discord!')


if __name__ == '__main__':

    asyncio.run(bot.start(TOKEN))
