from tasks import Task
import re
from datetime import datetime, timedelta

def get_next_weekday(day_name: str) -> datetime:
    # Map full day names to numbers (0=Monday, 6=Sunday)
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6
    }

    day_name_lower = day_name.lower()
    if day_name_lower not in weekdays:
        raise ValueError(f"Invalid day name: {day_name}")

    today = datetime.now()
    current_weekday = today.weekday()
    target_weekday = weekdays[day_name_lower]

    # Calculate the number of days to add to get to the next occurrence of the target weekday
    days_ahead = (target_weekday - current_weekday + 7) % 7
    if days_ahead == 0:
        days_ahead = 7  # Ensure it moves to the next occurrence, not today

    return today + timedelta(days=days_ahead)

def extract_data(input_string: str) -> dict:
    # Define the regular expression to extract each piece of information
    pattern = r"(.*?); duration (\d+)m; due ([^;]+); (\d)"

    # Match the input string
    match = re.match(pattern, input_string)

    if match:
        # Extract due date and time
        raw_due = match.group(3)
        due_date = None

        try:
            # Try parsing formats with specific dates
            if any(char.isdigit() for char in raw_due.split()[0]):
                if len(raw_due.split()) > 1:  # Contains time
                    due_date = datetime.strptime(raw_due, "%m/%d %I:%M%p")
                else:
                    due_date = datetime.strptime(raw_due, "%m/%d")
                    due_date = due_date.replace(year=datetime.now().year)
            else:
                if len(raw_due.split()) > 1:  # Contains time
                    day_name, time_part = raw_due.split(maxsplit=1)
                    due_date = get_next_weekday(day_name)
                    due_time = datetime.strptime(time_part, "%I:%M%p").time()
                    due_date = datetime.combine(due_date.date(), due_time)
                else:
                    # Handle weekday names only
                    due_date = get_next_weekday(raw_due)
        except ValueError:
            raise ValueError(f"Unable to parse due date: {raw_due}")

        # Map the matched groups to appropriate labels
        data = {
            "name": match.group(1),
            "duration": int(match.group(2)),
            "due": due_date,
            "priority": int(match.group(4))
        }
        return data
    else:
        raise ValueError("Input string doesn't match the expected format.")

def parse_query(input: str) -> Task:
    # desired input format:: {name}; duration {time in minutes}; due {day name (monday, etc.), (date)}; {0 meaning low priority, 1 meaning high priority}
    data = extract_data(input)
    new_task: Task = Task(data["name"], data["priority"], data["duration"], data["due"])
    
    return new_task
