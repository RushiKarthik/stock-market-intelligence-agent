from datetime import datetime, timedelta, timezone
import email.utils


def is_recent(date_string, hours=36):
    if not date_string:
        return False

    try:
        published = email.utils.parsedate_to_datetime(date_string)

        if published.tzinfo is None:
            published = published.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)

        age = now - published

        return timedelta(0) <= age <= timedelta(hours=hours)

    except Exception:
        return False