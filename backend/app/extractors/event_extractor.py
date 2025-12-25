from bs4 import BeautifulSoup
import re


def extract_event_data(html: str, url: str, source: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    def text(node):
        return node.get_text(" ", strip=True) if node else ""

    title = text(soup.find("h1")) or text(soup.find("h2"))

    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find("section")
        or soup.body
    )

    raw = re.sub(r"\s+", " ", text(main)).strip()

    if len(raw) < 100:
        raw = re.sub(r"\s+", " ", text(soup)).strip()

    return {
        "title": title,
        "link": url,
        "source": source,
        "raw_description": raw
    }
