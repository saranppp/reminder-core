from datetime import datetime, timedelta


def calculate_reminder_date(
    event_date,
    reminder_days
):

    return event_date - timedelta(
        days=reminder_days
    )


def should_remind(
    reminder_date
):

    now = datetime.now()

    return now >= reminder_date