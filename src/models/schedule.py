from dataclasses import dataclass
import datetime
from typing import Literal, Optional, Union

from sqlalchemy import Tuple 


@dataclass(frozen=True)
class Event:
    name: Literal['Start', 'Vote', 'End']
    time: str


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


    def get_next_event(self, current_day: str, current_hour: str) -> Optional[Tuple[str, str, Event]] :

        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        current_day_index = days.index(current_day.lower())
        
        # Check events for the current day
        for event in getattr(self, days[current_day_index], []):
            event_hour = event.time.split(":")[0]
            if event_hour > current_hour: 
                return 'today', current_day, event
        
        # Check events for the following days until the end of the week
        for i in range(1, 8 - current_day_index):
            next_day_index = (current_day_index + i) % 7
            for event in getattr(self, days[next_day_index], []): 
                indicator = 'tomorrow' if i == 1 else days[next_day_index]
                return indicator, days[next_day_index], event
        
        return None
    

    def check_events(self, current_datetime: datetime.datetime) -> Optional[Literal['Start', 'Vote', 'End']]:

        # Get the current day, hour and minute
        today = current_datetime.strftime("%A").lower()
        hour = current_datetime.strftime("%H")
        minute = int(current_datetime.strftime("%M")) // 10 * 10

        todays_event: Optional[list[Event]] = self.__dict__[today]
        if todays_event is None: return None

        for event in todays_event:
            event_time = datetime.strptime(event.time, "%H:%M")

            if event_time.strftime("%H") == hour and event_time.strftime("%M") == minute:
                return event.name
            


    def get_events_dates(self, start_time: datetime.datetime) -> Optional[dict[Literal['vote', 'end'], datetime.datetime]]:

        start_day = start_time.strftime("%A").lower()
        start_hour = start_time.strftime("%H")

        events_times = {}

        day_vote, vote_event = self.get_next_event(start_day, start_hour)
        if vote_event and vote_event.name == 'Vote':
            vote_time = datetime.datetime.strptime(vote_event.time, "%H:%M")
            delta_days = datetime.timedelta(days=(day_vote - start_time.weekday()))
            delta_hours = datetime.timedelta(hours=vote_time.hour, minutes=vote_time.minute)
            vote_datetime = start_time + delta_days + delta_hours
            events_times['vote'] = vote_datetime
        elif vote_event and vote_event.name != 'Vote':
            return None

        day_end, end_event = self.get_next_event(day_vote, vote_event)
        if end_event and end_event.name == 'End':
            end_time = datetime.datetime.strptime(end_event.time, "%H:%M")
            delta_days = datetime.timedelta(days=(day_end - start_time.weekday()))
            delta_hours = datetime.timedelta(hours=end_time.hour, minutes=end_time.minute)
            end_datetime = start_time + delta_days + delta_hours
            events_times['end'] = end_datetime
        elif end_event and end_event.name != 'End':
            return None

        return events_times
    
  
    


