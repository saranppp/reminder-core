
from search import search_web
from event_resolver import resolve_event


def find_release_date(entity):

    queries = [
        f'"{entity}" next upcoming movie sequel release date',
        f'"{entity}" next movie release date official',
        f'"{entity}" upcoming movie release date',
    ]

    all_results = []
    seen_urls = set()

    for query in queries:

        print(f"\nSearching: {query}")

        try:
            results = search_web(query, max_results=5)

            for result in results:
                url = result.get("url", "")

                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(result)

        except Exception as error:
            print(f"Search failed: {error}")

    if not all_results:
        return {
            "status": "unknown",
            "date": None,
            "confidence": "NONE",
            "candidates": [],
        }

    print(f"\nUnique search results: {len(all_results)}")

    resolved = resolve_event(all_results)

    for candidate in resolved.get("candidates", []):
        print(
            candidate["date"].date(),
            "|",
            candidate["title"],
            "|",
            candidate["source"],
        )

    return resolved
