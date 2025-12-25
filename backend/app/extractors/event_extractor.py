from bs4 import BeautifulSoup
import re

def extract_event_data(html: str, url: str, source: str):
    soup = BeautifulSoup(html, "html.parser")

    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)

    main = soup.find("main") or soup.body
    text = main.get_text(" ", strip=True) if main else ""

    text = re.sub(r"\s+", " ", text)

    return {
        "title": title,
        "link": url,
        "source": source,
        "raw_description": text
    }
