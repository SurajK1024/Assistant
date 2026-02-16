from sqlalchemy import text
from database import get_session
from database.reminder_orm import UserReminder
from datetime import datetime
import uuid
from langchain.tools import tool


class DBManager:

    # ---------------------------
    # Health Check
    # ---------------------------
    @staticmethod
    # @tool
    def health_check():
        """Performs a health check on the database connection."""
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
    # @tool
    def create_reminder(user_id, title, reminder_at_utc):
        """
        Create a new reminder for a user. 
        Note: Input reminder_at_utc as an ISO format string.
        """

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
            return {"status": "success", "message": "Created"}

        except Exception as e:
            session.rollback()
            return {"status": "error", "message": str(e)}

        finally:
            session.close()

    # ---------------------------
    # Fetch Upcoming
    # ---------------------------
    @staticmethod
    # @tool
    def fetch_upcoming(user_id:str):
        """Retrieve all upcoming reminders for a specific user, if None"""
        if user_id:
            session = get_session()
            try:
                now = datetime.now()

                reminders = (
                    session.query(UserReminder)
                    .filter(
                        UserReminder.user_id == user_id,
                        UserReminder.reminder_date >= now,
                        UserReminder.is_completed == 0
                    )
                    .all()
                )

                result = [
                    {
                        "id": r.id,
                        "title": r.title,
                        "reminder_at": str(r.reminder_date),
                        "category": r.category
                    }
                    for r in reminders
                ]

                return {"status": "success", "message": result}

            finally:
                session.close()
        return {"status": "error", "message": "Provide the `user_id`"}

    # ---------------------------
    # Mark Done
    # ---------------------------
    @staticmethod
    # @tool
    def mark_done(reminder_id):
        """Mark a reminder as completed in the database."""
        
        session = get_session()
        try:
            reminder = session.get(UserReminder, reminder_id)
            if not reminder:
                return {"status": "not_found"}

            reminder.is_completed = 1
            reminder.updated_at = datetime.now()
            session.commit()

            return {"status": "success", "message": "Updated"}

        except Exception as e:
            session.rollback()
            return {"status": "error", "message": str(e)}

        finally:
            session.close()
