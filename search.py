import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/154.0 Safari/537.36"
    )
}


def search_web(query, max_results=5):

    url = (
        "https://html.duckduckgo.com/html/?q="
        + quote(query)
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    results = []

    for result in soup.select(".result")[:max_results]:

        title_element = result.select_one(".result__title")
        link_element = result.select_one(".result__a")
        snippet_element = result.select_one(".result__snippet")

        if not title_element or not link_element:
            continue

        results.append({
            "title": title_element.get_text(" ", strip=True),
            "url": link_element.get("href"),
            "snippet": (
                snippet_element.get_text(" ", strip=True)
                if snippet_element
                else ""
            )
        })

    return results