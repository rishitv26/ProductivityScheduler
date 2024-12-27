from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.reminders import Reminder
from datetime import datetime, timezone, timedelta
from tasks import Task
import os

calendar = GoogleCalendar('varshneyrishit5@gmail.com', credentials_path=os.getcwd() + "\.credentials\credentials.json")
# get all times of busyness

def time_in_block(start: datetime, end: datetime, time: datetime) -> bool:
    return time.replace(tzinfo=timezone.utc) >= start and time <= end.replace(tzinfo=timezone.utc)

def get_free_time(task: Task) -> list:
    """
    Finds all free time slots between busy periods from the current time until the task's due time.
    :param task: Task object with a due datetime
    :return: List of lists representing free time slots [start, end]
    """

    free_busy = calendar.get_free_busy(time_min=datetime.now(), time_max=task.due)

    free_times = [[datetime.now(), None]]

    # get all free times
    for start, end in free_busy:
        if time_in_block(start, end, free_times[0][0]):
            free_times[0][0] = end
            continue
        
        free_times[-1][1] = start
        free_times.append([end, None])
    
    free_times[-1][1] = task.due
    
    end_duration: timedelta = free_times[-1][1].astimezone(timezone.utc) - free_times[-1][0].astimezone(timezone.utc)
    if end_duration.total_seconds() / 60 == 0:
        free_times.pop()
    
    return free_times

def get_free_time_with_durations(task: Task) -> list:
    """
    Finds all free time slots between busy periods from the current time until the task's due time, alongside the durations of the free times
    :param task: Task object with a due datetime
    :return: List of lists representing free time slots and duration integer in minutes [start, end, duration]
    """
    
    free_time = get_free_time(task)
    free_time_with_durations = []
    
    for i in free_time:
        duration: timedelta = i[1].astimezone(timezone.utc) - i[0].astimezone(timezone.utc)
        free_time_with_durations.append([i[0], i[1], duration.total_seconds() / 60])
    
    return free_time_with_durations

def save_in_calendar(start: datetime, end: datetime, task: Task) -> None:
    event = Event(
        summary=task.name,
        start=start,
        end=start + timedelta(minutes=task.duration),
        reminders = [
            Reminder(method="popup", minutes_before_start=10),  # Reminder 10 minutes before start
            Reminder(method="popup", minutes_before_start=0),   # Reminder at the start
            Reminder(method="email", minutes_before_start=10),  # Reminder 10 minutes before start
            Reminder(method="email", minutes_before_start=0),   # Reminder at the start
        ]
    )
    calendar.add_event(event)
