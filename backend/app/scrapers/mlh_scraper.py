# backend/app/scrapers/mlh_scraper.py

import logging
from typing import Dict, List, Tuple
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

from app.engine.base_scraper import BaseScraper
from app.services.scraper_service import fetch_html_playwright

LOG = logging.getLogger("MLHScraper")
LOG.setLevel(logging.INFO)


class MLHScraper(BaseScraper):
    """
    MLH scraper — FULL PAGE MODE
    - Extracts ALL event links from the season page
    - Extracts FULL HTML for each event (no fragile CSS selectors)
    - Leaves parsing of details to AI/LLM layer
    """

    def crawl(self, url: str) -> Tuple[Dict, List[str]]:
        parsed = urlparse(url)

        # =======================================================================
        # LIST PAGE HANDLER: https://mlh.io/seasons/2025/events
        # =======================================================================
        if "mlh.io/seasons" in url and url.endswith("/events"):
            LOG.info("[MLH] Fetching MLH event list page (HTML + JS)")

            html = fetch_html_playwright(url)
            if not html:
                LOG.warning("[MLH] Could not fetch MLH events page")
                return None, []

            soup = BeautifulSoup(html, "html.parser")

            event_links = []

            # ANY <a> tag that contains "/events/" → treat as event link
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "/events/" not in href:
                    continue

                abs_url = urljoin(url, href)
                if abs_url not in event_links:
                    event_links.append(abs_url)
                    LOG.info(f"[MLH] EVENT FOUND → {abs_url}")

            LOG.info(f"[MLH] TOTAL EVENTS FOUND: {len(event_links)}")

            return None, event_links

        # =======================================================================
        # DETAIL PAGE HANDLER: https://mlh.io/events/xxxx
        # =======================================================================
        if parsed.netloc.endswith("mlh.io") and "/events/" in parsed.path:
            LOG.info(f"[MLH] Fetching FULL EVENT PAGE: {url}")

            html = fetch_html_playwright(url)
            if not html:
                LOG.warning(f"[MLH] Failed to load event detail page: {url}")
                return None, []

            soup = BeautifulSoup(html, "html.parser")

            # Try a weak title extraction (non-critical)
            title_el = soup.find("h1") or soup.find("h2")
            title = title_el.get_text(strip=True) if title_el else ""

            data = {
                "title": title,
                "link": url,
                "source": "MLH",
                "raw_html": html   # FULL HTML for LLM processing later
            }

            return data, []

        # =======================================================================
        # UNKNOWN URL — do nothing
        # =======================================================================
        return None, []
