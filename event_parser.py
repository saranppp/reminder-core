import re


def parse_reminder(text: str):
    text = text.strip()

    text_lower = text.lower()

    reminder_days = 0

    # --------------------------------
    # Detect reminder offset
    # --------------------------------

    match = re.search(
        r"(\d+)\s+days?\s+before",
        text_lower
    )

    if match:
        reminder_days = int(match.group(1))

    elif "week before" in text_lower:
        reminder_days = 7

    elif "month before" in text_lower:
        reminder_days = 30

    # --------------------------------
    # Detect event type from text
    # --------------------------------

    event_type = detect_event_type(text_lower)

    # --------------------------------
    # Extract entity
    # --------------------------------

    entity = extract_entity(
        text_lower,
        event_type
    )

    return {
        "original_text": text,
        "event_type": event_type,
        "entity": entity,
        "reminder_days": reminder_days
    }


def detect_event_type(text):

    if any(word in text for word in [
        "movie",
        "film",
        "cinema"
    ]):
        return "movie_release"

    if any(word in text for word in [
        "game",
        "gaming"
    ]):
        return "game_release"

    if any(word in text for word in [
        "concert",
        "concerts",
        "event"
    ]):
        return "concert"

    if any(word in text for word in [
        "phone",
        "iphone",
        "pixel",
        "product"
    ]):
        return "product_release"

    return "unknown"


def extract_entity(text, event_type):

    if event_type == "movie_release":

        patterns = [
            r"next (.+?) movie",
            r"(.+?) movie",
            r"movie (.+?) released",
            r"movie (.+?) release"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text
            )

            if match:

                entity = match.group(1).strip()

                entity = re.sub(
                    r"\b(is|the|when|about|to|be|released|release)\b",
                    "",
                    entity
                )

                return entity.strip()

    # If we don't know the type yet,
    # assume the complete input is the entity.

    return text