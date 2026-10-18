import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def search_web(query, max_results=5):

    url = (
        "https://www.bing.com/search?q="
        + quote(query)
    )

    print(f"\nSearch URL: {url}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    print(f"HTTP status: {response.status_code}")

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    results = []

    for result in soup.select("li.b_algo"):

        title_element = result.select_one("h2 a")
        snippet_element = result.select_one(".b_caption p")

        if not title_element:
            continue

        title = title_element.get_text(
            " ",
            strip=True
        )

        link = title_element.get("href")

        snippet = ""

        if snippet_element:
            snippet = snippet_element.get_text(
                " ",
                strip=True
            )

        results.append({
            "title": title,
            "url": link,
            "snippet": snippet
        })

        if len(results) >= max_results:
            break

    return results