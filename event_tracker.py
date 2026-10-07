import re
from datetime import datetime

from search import search_web


MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def find_release_date(entity):

    query = (
        f"{entity} movie release date "
        f"official upcoming"
    )

    print(f"\nSearching web for:")
    print(query)

    results = search_web(query)

    if not results:
        print("No search results found.")

        return {
            "status": "unknown",
            "date": None,
            "sources": []
        }

    print(f"\nFound {len(results)} search results:")

    for index, result in enumerate(results, 1):

        print(
            f"\n[{index}] {result['title']}"
        )

        print(
            result["snippet"]
        )

    # Combine title + snippet
    text = " ".join(
        result["title"] + " " + result["snippet"]
        for result in results
    )

    release_date = extract_date(text)

    if release_date:

        return {
            "status": "date_found",
            "date": release_date,
            "sources": results
        }

    return {
        "status": "unknown",
        "date": None,
        "sources": results
    }


def extract_date(text):

    text = text.lower()

    # --------------------------------
    # Pattern:
    # May 20, 2027
    # --------------------------------

    pattern = (
        r"\b("
        + "|".join(MONTHS.keys())
        + r")\s+"
        r"(\d{1,2}),?\s+"
        r"(\d{4})"
    )

    matches = re.findall(pattern, text)

    for month, day, year in matches:

        try:

            date = datetime(
                int(year),
                MONTHS[month],
                int(day)
            )

            return date

        except ValueError:
            continue

    # --------------------------------
    # Pattern:
    # May 2027
    # --------------------------------

    pattern = (
        r"\b("
        + "|".join(MONTHS.keys())
        + r")\s+"
        r"(\d{4})"
    )

    matches = re.findall(pattern, text)

    for month, year in matches:

        try:

            date = datetime(
                int(year),
                MONTHS[month],
                1
            )

            return date

        except ValueError:
            continue

    return None