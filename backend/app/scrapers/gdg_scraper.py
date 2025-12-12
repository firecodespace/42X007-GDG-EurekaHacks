import logging
from typing import List, Dict
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.utils.cleaner import normalize_event

from playwright.sync_api import sync_playwright

LOG = logging.getLogger("gdg_scraper")
LOG.setLevel(logging.INFO)

GDG_EVENTS_URL = "https://gdg.community.dev/events/"

def parse_date(text: str):
    try:
        from dateutil import parser
        return parser.parse(text, fuzzy=True).isoformat()
    except:
        return text.strip()

def scrape_gdg_events(limit: int = 50) -> List[Dict]:
    events = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        LOG.info("Navigating to GDG events page...")
        page.goto(GDG_EVENTS_URL, timeout=60000)

        # Wait for event cards to load
        page.wait_for_selector("a[href*='/events/']", timeout=60000)

        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        browser.close()

    cards = soup.select("a[href*='/events/']")

    seen = set()

    for card in cards:
        link = card.get("href")
        if not link or "/events/" not in link:
            continue

        full_link = urljoin(GDG_EVENTS_URL, link)

        if full_link in seen:
            continue
        seen.add(full_link)

        title = card.get_text(strip=True)
        parent = card.parent

        # Try to find a date nearby
        date_node = parent.select_one("time") or parent.find("div", string=lambda x: "20" in str(x))
        date = parse_date(date_node.get_text(strip=True)) if date_node else ""

        event = {
            "title": title or "GDG Event",
            "link": full_link,
            "source": "GDG",
            "location": "Online / TBD",
            "deadline": date,
            "raw_description": "",
        }

        events.append(normalize_event(event))

        if len(events) >= limit:
            break

    LOG.info("Scraped %d GDG events", len(events))
    return events
