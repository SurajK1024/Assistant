import dateparser
import pytz
from datetime import datetime


def parse_datetime_to_utc(text, user_timezone="Asia/Kolkata"):
    """
    Convert natural language datetime into UTC timestamp
    """

    settings = {
        "TIMEZONE": user_timezone,
        "RETURN_AS_TIMEZONE_AWARE": True,
        "PREFER_DATES_FROM": "future"
    }

    dt = dateparser.parse(text, settings=settings)

    if not dt:
        return {
            "status": "error",
            "message": "Could not parse datetime"
        }

    utc_dt = dt.astimezone(pytz.utc)

    return {
        "status": "success",
        "datetime_utc": utc_dt
    }
