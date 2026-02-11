from sqlalchemy import Column, BigInteger, String, Text, Date, Time, DateTime, Enum, Integer, Float
from . import Base

class UserReminder(Base):
    __tablename__ = "user_reminders"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    user_id = Column(BigInteger)

    category = Column(Enum('EVENT','TASK','REMINDER','GENERAL'))

    title = Column(String(191))
    description = Column(Text)

    reminder_date = Column(Date)
    reminder_time = Column(Time)
    reminder_at_utc = Column(DateTime)

    meeting_link = Column(String(191))

    reminder_type = Column(Enum(
        'NONE','ONE_DAY_BEFORE','TWO_HOURS_BEFORE',
        'ONE_HOUR_BEFORE','THIRTY_MIN_BEFORE',
        'FIFTEEN_MIN_BEFORE','FIVE_MIN_BEFORE','ON_TIME'
    ))

    is_recurring = Column(Integer)
    recurrence_pattern = Column(Enum(
        'NEVER','DAILY','WEEKDAYS','WEEKENDS','WEEKLY',
        'FORTNIGHTLY','MONTHLY','EVERY_3_MONTH',
        'EVERY_6_MONTH','YEARLY'
    ))

    recurrence_end_date = Column(String(191))

    snooze_duration = Column(Integer)
    snooze_count = Column(Integer)

    location = Column(String(191))
    latitude = Column(Float)
    longitude = Column(Float)

    priority = Column(Enum('NONE','LOW','MEDIUM','HIGH'))
    color = Column(String(191))

    status = Column(Integer)
    is_completed = Column(Integer)

    outlook_id = Column(String(200))
    google_id = Column(String(200))
    apple_id = Column(String(191))

    last_sent_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user_family_friend_id = Column(BigInteger)
