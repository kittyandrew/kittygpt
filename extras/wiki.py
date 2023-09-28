from urllib.parse import quote
import re

import requests

HTML_TAG_CLEANER = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")


def wiki_search(query: str):
    """Return the results of a Wikipedia search"""
    search_url = "https://en.wikipedia.org/w/api.php?action=query&format=json" \
        f"&list=search&utf8=1&formatversion=2&srsearch={quote(query)}"
    with requests.Session() as session:
        session.headers.update({"Accept": "application/json", "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36"
        )})
        result = session.get(search_url).json()

    items, max_results = [], 3
    for item in result["query"]["search"]:
        summary = re.sub(HTML_TAG_CLEANER, "", item["snippet"])
        items.append({  # Isn't markdown text a better format for this?
            "title": item["title"], "summary": summary,
            "url": f"http://en.wikipedia.org/?curid={item['pageid']}",
        })
        if len(items) == max_results: break
    return items
