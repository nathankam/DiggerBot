from dataclasses import dataclass
import datetime
import pytz
from typing import Literal, Optional, Union


@dataclass(frozen=True)
class Event:
    name: Literal['Start', 'Vote', 'End']
    time: str
    
    # Get the event datetime in UTC based on the timezone and the day of the week 
    def get_event_datetime_utc(
            self, 
            event_timezone: str,
            event_day: Literal['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'], 
            now_utc : datetime.datetime = datetime.datetime.now(pytz.utc)
    ) -> datetime.datetime:
            
        # Give 'NOW' to the function
        tz = pytz.timezone(event_timezone) 
        now_tz = now_utc.astimezone(tz)  #8h -> 9h
        today = now_tz.strftime("%A").lower()

        # Event TIME
        event_hour_tz = datetime.datetime.strptime(self.time, "%H:%M")

        # If the event is today 
        if event_day == today:
            event_time_tz = datetime.datetime.combine(now_tz.date(), event_hour_tz.time()).replace(tzinfo=tz)
            return event_time_tz.astimezone(pytz.utc)
        
        # if the event is some day within the rest of the week 
        delta_day = (datetime.datetime.strptime(event_day, "%A").weekday() - 
                     datetime.datetime.strptime(today, "%A").weekday())
        
        date_event = now_tz.date() + datetime.timedelta(days=delta_day)
        event_time = datetime.datetime.combine(date_event, event_hour_tz.time()).replace(tzinfo=tz)

        return event_time.astimezone(pytz.utc)
    

@dataclass(frozen=True)
class Schedule:
    id: int
    name: str
    description: str
    monday: Optional[list[Event]] = None
    tuesday: Optional[list[Event]] = None
    wednesday: Optional[list[Event]] = None
    thursday: Optional[list[Event]] = None
    friday: Optional[list[Event]] = None
    saturday: Optional[list[Event]] = None
    sunday: Optional[list[Event]] = None
    

    # Get the next events for the week
    def get_next_events(self, start_time: datetime.datetime, timezone: str) -> Optional[list[tuple[str, Event]]]:

        # Get the day of the week and the hour
        tz = pytz.timezone(timezone)
        start_time_tz = start_time.astimezone(tz)
        day = start_time_tz.strftime("%A")
        hour = start_time_tz.strftime("%H")
        minute = start_time_tz.strftime("%M")

        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        current_day_index = days.index(day.lower())

        next_events = []

        # Check events for the current day (comparison of tz hours)
        for event in getattr(self, days[current_day_index], []):
            event_time = datetime.datetime.strptime(event.time, "%H:%M")
            event_hour = event_time.strftime("%H")
            if int(event_hour) > int(hour): 
                next_events.append((day, event))

        # Check events for the following days until the end of the week        
        for i in range(1, 8 - current_day_index):
            next_day_index = (current_day_index + i) % 7
            for event in getattr(self, days[next_day_index], []): 
                next_events.append((days[next_day_index], event))

        return next_events


    # Check the current event
    def check_events(self, now_utc: datetime.datetime, timezone: str) -> Optional[Literal['Start', 'Vote', 'End']]:

        # Get the current day, hour and minute
        today = now_utc.strftime("%A").lower()
        hour = int(now_utc.strftime("%H"))
        minute = int(now_utc.strftime("%M")) // 10 * 10

        # Get today's events
        todays_event: Optional[list[Event]] = self.__dict__[today]
        if todays_event is None: return None

        # Events are stated as %HH:%MM in the group's timezone
        events = []
        for event in todays_event:
            utc_event_time = event.get_event_datetime_utc(timezone, today, now_utc)
            print('[TEST-LOG]', event.name, now_utc, utc_event_time)
            if utc_event_time.hour == hour and utc_event_time.minute == minute:
                events.append(event.name)

        return events[0] if len(events) > 0 else None
            

    # Get the next events dates // within the same week 
    def get_events_dates(self, start_time: datetime.datetime, timezone: str) -> Optional[dict[Literal['vote', 'end'], datetime.datetime]]:

        # Get the next events
        all_events = self.get_next_events(start_time, timezone)
        next_vote_events = [(d, e) for d, e in all_events if e.name == 'Vote']
        next_end_events = [(d, e) for d, e in all_events if e.name == 'End']
        next_vote_event = next_vote_events[0] if len(next_vote_events) > 0 else None
        next_end_event = next_end_events[0] if len(next_end_events) > 0 else None 

        # Events datetimes 
        vote_event_time = next_vote_event[1].get_event_datetime_utc(timezone, next_vote_event[0], start_time) if next_vote_event else None
        end_event_time = next_end_event[1].get_event_datetime_utc(timezone, next_end_event[0], start_time) if next_end_event else None

        return {'vote': vote_event_time, 'end': end_event_time}

    
  
    


