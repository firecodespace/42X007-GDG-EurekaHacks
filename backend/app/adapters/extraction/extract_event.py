from bs4 import BeautifulSoup

from app.domain.entities.event import Event
from app.domain.entities.fetched_page import FetchedPage


def extract_event(page: FetchedPage) -> Event:
    soup = BeautifulSoup(page.html, "html.parser")
    title = (soup.select_one("h1") or soup.select_one("title"))
    title_text = title.get_text(strip=True) if title else page.url
    return Event(title=title_text, url=page.url, source=page.source, description=None)
