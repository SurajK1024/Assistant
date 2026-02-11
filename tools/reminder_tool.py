from database import get_session
from database.reminder_orm import UserReminder
import uuid
from datetime import datetime
from typing import Literal


def create_reminder(user_id, title, reminder_at_utc, category: Literal["EVENT", "TASK", "REMINDER", "GENERAL"] = "REMINDER"):
    session = get_session()

    reminder = UserReminder(
        uuid=str(uuid.uuid4()),
        user_id=user_id,
        title=title,
        category=category,
        reminder_at_utc=reminder_at_utc,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        status=1,
        is_completed=0
    )

    session.add(reminder)
    session.commit()
    session.close()

    return {"status": "created"}
