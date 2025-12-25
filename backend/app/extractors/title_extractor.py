# app/extractors/title_extractor.py

from bs4 import BeautifulSoup

def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Priority order
    selectors = [
        "h1",
        "meta[property='og:title']",
        "title"
    ]

    for sel in selectors:
        el = soup.select_one(sel)
        if el:
            if el.name == "meta":
                return el.get("content", "").strip()
            return el.get_text(strip=True)

    return ""
