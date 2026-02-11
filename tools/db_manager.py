from sqlalchemy import text
from database import get_session
from database.reminder_orm import UserReminder
from datetime import datetime
import uuid


class DBManager:

    # ---------------------------
    # Health Check
    # ---------------------------
    @staticmethod
    def health_check():
        session = None
        try:
            session = get_session()
            session.execute(text("SELECT 1"))
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if session:
                session.close()

    # ---------------------------
    # Create Reminder
    # ---------------------------
    @staticmethod
    def create_reminder(user_id, title, reminder_at_utc):
        session = get_session()
        try:
            reminder = UserReminder(
                uuid=str(uuid.uuid4()),
                user_id=user_id,
                title=title,
                reminder_at_utc=reminder_at_utc,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                status=1,
                is_completed=0
            )

            session.add(reminder)
            session.commit()
            return {"status": "created"}

        except Exception as e:
            session.rollback()
            return {"status": "error", "message": str(e)}

        finally:
            session.close()

    # ---------------------------
    # Fetch Upcoming
    # ---------------------------
    @staticmethod
    def fetch_upcoming(user_id):
        session = get_session()
        try:
            now = datetime.now()

            reminders = (
                session.query(UserReminder)
                .filter(
                    UserReminder.user_id == user_id,
                    UserReminder.reminder_at_utc >= now,
                    UserReminder.is_completed == 0
                )
                .all()
            )

            result = [
                {
                    "id": r.id,
                    "title": r.title,
                    "reminder_at": str(r.reminder_at_utc)
                }
                for r in reminders
            ]

            return result

        finally:
            session.close()

    # ---------------------------
    # Mark Done
    # ---------------------------
    @staticmethod
    def mark_done(reminder_id):
        session = get_session()
        try:
            reminder = session.get(UserReminder, reminder_id)
            if not reminder:
                return {"status": "not_found"}

            reminder.is_completed = 1
            reminder.updated_at = datetime.now()
            session.commit()

            return {"status": "completed"}

        except Exception as e:
            session.rollback()
            return {"status": "error", "message": str(e)}

        finally:
            session.close()
