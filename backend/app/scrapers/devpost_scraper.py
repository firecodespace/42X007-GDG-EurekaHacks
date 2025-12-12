# app/scrapers/devpost_scraper.py

import logging
from typing import Tuple, Dict, List
from urllib.parse import urlparse

from app.engine.base_scraper import BaseScraper
from app.services.scraper_service import fetch_html
from bs4 import BeautifulSoup

LOG = logging.getLogger("DevpostScraper")
LOG.setLevel(logging.INFO)


class DevpostScraper(BaseScraper):

    def crawl(self, url: str) -> Tuple[Dict, List[str]]:
        """
        Router for Devpost domains.
        Handles:
            - devpost.com/hackathons (list page)
            - *.devpost.com (individual hackathons)
        """

        parsed = urlparse(url)

        # -------------------------
        # CASE 1: List page
        # -------------------------
        if parsed.netloc == "devpost.com" and "/hackathons" in parsed.path:
            LOG.info(f"[Devpost] Crawling list page: {url}")

            html = fetch_html(url)
            if not html:
                return None, []

            soup = BeautifulSoup(html, "html.parser")

            # Extract event links
            links = []
            for a in soup.select("a"):
                href = a.get("href", "")
                if href.startswith("https://") and "devpost.com" in href:
                    links.append(href)
                elif "/hackathons/" in href:
                    links.append("https://devpost.com" + href)

            LOG.info(f"[Devpost] Found {len(links)} detail links")
            return None, links

        # -------------------------
        # CASE 2: Individual event page
        # -------------------------
        if parsed.netloc.endswith("devpost.com"):
            LOG.info(f"[Devpost] Crawling event page: {url}")

            html = fetch_html(url)
            if not html:
                return None, []

            soup = BeautifulSoup(html, "html.parser")

            title_el = soup.select_one("h1, .title, .challenge-title")
            title = title_el.get_text(strip=True) if title_el else ""

            desc_el = soup.select_one(".challenge-description, .content, p")
            desc = desc_el.get_text(strip=True) if desc_el else ""

            deadline_el = soup.select_one(".submission-deadline-date, time")
            deadline = deadline_el.get_text(strip=True) if deadline_el else ""

            location_el = soup.select_one(".locations, .challenge-location")
            location = location_el.get_text(strip=True) if location_el else "Online"

            data = {
                "title": title,
                "link": url,
                "source": "Devpost",
                "location": location,
                "deadline": deadline,
                "raw_description": desc,
            }

            return data, []  # no further links for now

        # -------------------------
        # CASE 3: Unknown pattern
        # -------------------------
        return None, []
