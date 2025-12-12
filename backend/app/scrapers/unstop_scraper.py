# app/scrapers/unstop_scraper.py

import logging
from typing import Tuple, Dict, List
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

from app.engine.base_scraper import BaseScraper
from app.services.scraper_service import fetch_html

LOG = logging.getLogger("UnstopScraper")
LOG.setLevel(logging.INFO)


class UnstopScraper(BaseScraper):
    """
    Handles:
        - https://unstop.com/competitions (list)
        - any event pages under /competition/<slug>
    """

    def crawl(self, url: str) -> Tuple[Dict, List[str]]:
        parsed = urlparse(url)

        # -----------------------------------
        # CASE 1: LIST PAGE
        # -----------------------------------
        if "unstop.com" in parsed.netloc and "/competitions" in parsed.path:
            LOG.info(f"[Unstop] Crawling list page: {url}")

            html = fetch_html(url)
            if not html:
                return None, []

            soup = BeautifulSoup(html, "html.parser")

            links = []
            for a in soup.select("a"):
                href = a.get("href", "")
                if "/competition/" in href:
                    abs_url = urljoin(url, href)
                    links.append(abs_url)

            LOG.info(f"[Unstop] Found {len(links)} event links")
            return None, links

        # -----------------------------------
        # CASE 2: EVENT PAGE
        # -----------------------------------
        if "unstop.com" in parsed.netloc and "/competition/" in parsed.path:
            LOG.info(f"[Unstop] Crawling event page: {url}")

            html = fetch_html(url)
            if not html:
                return None, []

            soup = BeautifulSoup(html, "html.parser")

            # Title
            title_el = soup.select_one("h1, .heading, .event-title")
            title = title_el.get_text(strip=True) if title_el else ""

            # Description
            desc_el = soup.select_one(".description, .event-description, p")
            desc = desc_el.get_text(strip=True) if desc_el else ""

            # Deadline
            deadline_el = soup.find("i", {"class": "uil-calendar"})
            deadline = ""
            if deadline_el and deadline_el.parent:
                deadline = deadline_el.parent.get_text(strip=True)

            # Location
            loc_el = soup.find("i", {"class": "uil-map-marker"})
            location = ""
            if loc_el and loc_el.parent:
                location = loc_el.parent.get_text(strip=True)

            data = {
                "title": title,
                "link": url,
                "source": "Unstop",
                "location": location or "Online",
                "deadline": deadline,
                "raw_description": desc,
            }

            return data, []

        # -----------------------------------
        # CASE 3: Not relevant
        # -----------------------------------
        return None, []
