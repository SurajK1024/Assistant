from datetime import datetime, timedelta
from tools.db_manager import DBManager
from typing import Literal


REMINDER_TYPE_MAP = {
    "ONE_DAY_BEFORE"    : timedelta(days=1),
    "ONE_HOUR_BEFORE"   : timedelta(hours=1),
    "THIRTY_MIN_BEFORE" : timedelta(minutes=30),
    "FIVE_MIN_BEFORE"   : timedelta(minutes=5),
    "ON_TIME"           : timedelta(seconds=0)
}


def generate_reminder_plan(user_id, title, event_time_utc, reminder_types, category: Literal["EVENT", "TASK", "REMINDER", "GENERAL"] = "REMINDER"):

    created = []

    for rtype in reminder_types:
        offset = REMINDER_TYPE_MAP[rtype]

        reminder_time = event_time_utc - offset

        DBManager.create_reminder(
            user_id=user_id,
            title=f"{title} ({rtype})",
            reminder_date=datetime.strftime(event_time_utc, format="%Y-%m-%d"),
            reminder_time=datetime.strftime(event_time_utc, format="%H:%M:%S"),
            category=category
        )

        created.append({
            "type": rtype,
            "scheduled_at": reminder_time
        })

    return created
