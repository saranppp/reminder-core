from datetime import datetime

from event_parser import parse_reminder

from event_tracker import find_release_date

from database import (
    initialize_database,
    create_reminder,
    update_event,
    get_reminder,
    get_active_reminders
)

from scheduler import (
    calculate_reminder_date,
    should_remind
)


def create_new_reminder():

    user_input = input(
        "\nWhat should I remind you about?\n> "
    )

    parsed = parse_reminder(user_input)

    print("\n-----------------------------")
    print("PARSED REQUEST")
    print("-----------------------------")

    print(
        f"Event type:     {parsed['event_type']}"
    )

    print(
        f"Entity:         {parsed['entity']}"
    )

    print(
        f"Days before:    {parsed['reminder_days']}"
    )

    if parsed["event_type"] == "unknown":

        print(
            "\nEvent type is not supported yet."
        )

        return

    reminder_id = create_reminder(
        user_text=user_input,
        event_type=parsed["event_type"],
        entity=parsed["entity"],
        reminder_days=parsed["reminder_days"]
    )

    print(
        f"\nReminder created with ID: {reminder_id}"
    )

    check_reminder(reminder_id)


def check_reminder(reminder_id):

    reminder = get_reminder(reminder_id)

    if not reminder:

        print("Reminder not found.")

        return

    # Database columns
    entity = reminder[3]
    reminder_days = reminder[4]

    print("\n=============================")
    print("CHECKING EVENT")
    print("=============================")

    result = find_release_date(entity)

    if result["date"] is None:

        print(
            "\nCould not determine the release date."
        )

        return

    event_date = result["date"]

    reminder_date = calculate_reminder_date(
        event_date,
        reminder_days
    )

    update_event(
        reminder_id,
        event_date.isoformat(),
        reminder_date.isoformat()
    )

    print("\n=============================")
    print("EVENT STATE")
    print("=============================")

    print(
        f"Event:          {entity}"
    )

    print(
        f"Release date:   {event_date.date()}"
    )

    print(
        f"Reminder date:  {reminder_date.date()}"
    )

    if should_remind(reminder_date):

        print(
            "\n🔔 REMINDER SHOULD FIRE!"
        )

    else:

        days_until = (
            reminder_date - datetime.now()
        ).days

        print(
            f"\nReminder is approximately "
            f"{days_until} days away."
        )


def check_all_reminders():

    reminders = get_active_reminders()

    print(
        f"\nChecking {len(reminders)} active reminders..."
    )

    for reminder in reminders:

        reminder_id = reminder[0]

        check_reminder(reminder_id)


def main():

    initialize_database()

    while True:

        print("\n")
        print("=============================")
        print("      EVENT REMINDER")
        print("=============================")

        print("1. Create reminder")
        print("2. Check all reminders")
        print("3. Exit")

        choice = input("\nSelect: ")

        if choice == "1":

            create_new_reminder()

        elif choice == "2":

            check_all_reminders()

        elif choice == "3":

            break

        else:

            print("Invalid choice.")


if __name__ == "__main__":

    main()