# backend/app/scrapers/mlh_scraper.py

import logging
from typing import Dict, List, Tuple
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

from app.engine.base_scraper import BaseScraper
from app.services.scraper_service import fetch_html
from app.utils.extractor import extract_event_data   # <<– structured extractor

LOG = logging.getLogger("MLHScraper")
LOG.setLevel(logging.INFO)


class MLHScraper(BaseScraper):
    """
    MLH scraper — STRUCTURED MODE
    Extract only human-visible structured info:
    - title
    - description
    - date/deadline
    - location
    - tags
    No raw HTML stored.
    """

    def crawl(self, url: str) -> Tuple[Dict, List[str]]:
        parsed = urlparse(url)

        # ============================================================
        # LIST PAGE
        # ============================================================
        if "mlh.io/seasons" in url and url.endswith("/events"):
            LOG.info("[MLH] Fetching MLH event list page")

            html = fetch_html(url, force_browser=True)
            if not html:
                LOG.warning("[MLH] Could not load MLH event list")
                return None, []

            soup = BeautifulSoup(html, "html.parser")
            event_links = []

            # <a href="/events/xxxx">
            for a in soup.find_all("a", href=True):
                href = a["href"]

                if "/events/" not in href:
                    continue

                abs_url = urljoin(url, href)
                if abs_url not in event_links:
                    event_links.append(abs_url)
                    LOG.info(f"[MLH] Event URL → {abs_url}")

            LOG.info(f"[MLH] Total events discovered: {len(event_links)}")

            return None, event_links

        # ============================================================
        # DETAIL PAGE
        # ============================================================
        if parsed.netloc.endswith("mlh.io") and "/events/" in parsed.path:
            LOG.info(f"[MLH] Fetching event detail page → {url}")

            html = fetch_html(url, force_browser=True)
            if not html:
                LOG.warning(f"[MLH] Failed to load event detail: {url}")
                return None, []

            # Use the unified structured extractor
            data = extract_event_data(html, url, "MLH")

            return data, []

        # ============================================================
        # NOT MLH → IGNORE
        # ============================================================
        return None, []
