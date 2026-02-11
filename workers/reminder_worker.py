import time
from datetime import datetime, timedelta
from tools.db_manager import DBManager
from tools.notification_tools import send_notification


CHECK_INTERVAL = 60   # seconds


def reminder_loop(user_id, days:int=7):

    print("Reminder worker started...")

    while True:
        try:
            now = datetime.now()
            upcoming_window = now + timedelta(days=days)

            reminders = DBManager.fetch_upcoming(user_id=user_id)

            for r in reminders:
                reminder_time = datetime.fromisoformat(r["reminder_at"])

                if now <= reminder_time <= upcoming_window:
                    send_notification(
                        user_id=user_id,
                        message=f"{r['category']}: {r['title']}",
                        date=r['reminder_at'],
                    )

                    # DBManager.mark_done(r["id"])

        except Exception as e:
            print("Worker error:", e)

        print(f"Worker sleeping for {CHECK_INTERVAL} seconds...")
        time.sleep(CHECK_INTERVAL)