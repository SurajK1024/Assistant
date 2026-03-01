from sqlalchemy import Column, BigInteger, String, Text, Date, Time, DateTime, Enum, Integer, Float
from . import Base

class UserReminder(Base):
    __tablename__ = "user_reminders"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    # REQUIRED
    user_id = Column(BigInteger, nullable=False)
    title = Column(String(191), nullable=False)

    # OPTIONAL
    uuid = Column(String(36), nullable=True)

    category = Column(Enum('EVENT','TASK','REMINDER','GENERAL'), nullable=True)
    description = Column(Text, nullable=True)

    reminder_date = Column(Date, nullable=True)
    reminder_time = Column(Time, nullable=True)
    reminder_at_utc = Column(DateTime, nullable=True)

    meeting_link = Column(String(191), nullable=True)

    reminder_type = Column(Enum(
        'NONE','ONE_DAY_BEFORE','TWO_HOURS_BEFORE',
        'ONE_HOUR_BEFORE','THIRTY_MIN_BEFORE',
        'FIFTEEN_MIN_BEFORE','FIVE_MIN_BEFORE','ON_TIME'
    ), nullable=True)

    is_recurring = Column(Integer, default=0)
    recurrence_pattern = Column(Enum(
        'NEVER','DAILY','WEEKDAYS','WEEKENDS','WEEKLY',
        'FORTNIGHTLY','MONTHLY','EVERY_3_MONTH',
        'EVERY_6_MONTH','YEARLY'
    ), nullable=True)

    recurrence_end_date = Column(String(191), nullable=True)

    snooze_duration = Column(Integer, nullable=True)
    snooze_count = Column(Integer, nullable=True)

    location = Column(String(191), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    priority = Column(Enum('NONE','LOW','MEDIUM','HIGH'), nullable=True)
    color = Column(String(191), nullable=True)

    status = Column(Integer, default=1)
    is_completed = Column(Integer, default=0)

    outlook_id = Column(String(200), nullable=True)
    google_id = Column(String(200), nullable=True)
    apple_id = Column(String(191), nullable=True)

    last_sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user_family_friend_id = Column(BigInteger, nullable=True)