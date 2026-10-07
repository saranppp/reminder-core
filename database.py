import sqlite3
from datetime import datetime


DB_NAME = "reminders.db"


def get_connection():

    return sqlite3.connect(DB_NAME)


def initialize_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS reminders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_text TEXT NOT NULL,

            event_type TEXT NOT NULL,

            entity TEXT NOT NULL,

            reminder_days INTEGER NOT NULL,

            event_date TEXT,

            reminder_date TEXT,

            status TEXT NOT NULL,

            last_checked TEXT,

            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_reminder(
    user_text,
    event_type,
    entity,
    reminder_days
):

    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO reminders (
            user_text,
            event_type,
            entity,
            reminder_days,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_text,
        event_type,
        entity,
        reminder_days,
        "active",
        datetime.now().isoformat()
    ))

    reminder_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return reminder_id


def get_reminder(reminder_id):

    conn = get_connection()

    cursor = conn.execute("""
        SELECT *
        FROM reminders
        WHERE id = ?
    """, (reminder_id,))

    result = cursor.fetchone()

    conn.close()

    return result


def update_event(
    reminder_id,
    event_date,
    reminder_date
):

    conn = get_connection()

    conn.execute("""
        UPDATE reminders
        SET
            event_date = ?,
            reminder_date = ?,
            last_checked = ?
        WHERE id = ?
    """, (
        event_date,
        reminder_date,
        datetime.now().isoformat(),
        reminder_id
    ))

    conn.commit()
    conn.close()


def get_active_reminders():

    conn = get_connection()

    cursor = conn.execute("""
        SELECT *
        FROM reminders
        WHERE status = 'active'
    """)

    results = cursor.fetchall()

    conn.close()

    return results