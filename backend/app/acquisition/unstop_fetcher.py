import logging
import json
from typing import Optional
import requests
from bs4 import BeautifulSoup

from app.acquisition.fetched_page import FetchedPage
from app.discovery.discovered_url import DiscoveredURL
from app.utils.time import utc_now

LOG = logging.getLogger("UnstopFetcher")


class UnstopFetcher:
    """
    Fetches Unstop opportunity data from __NEXT_DATA__.
    """

    def fetch(self, discovered: DiscoveredURL) -> Optional[FetchedPage]:
        try:
            resp = requests.get(
                discovered.url,
                timeout=20,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            resp.raise_for_status()
        except Exception as exc:
            LOG.error("Unstop fetch failed for %s", discovered.url, exc_info=exc)
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")

        if not script:
            LOG.warning("No __NEXT_DATA__ found for %s", discovered.url)
            return None

        try:
            data = json.loads(script.string)
        except Exception as exc:
            LOG.error("Failed to parse __NEXT_DATA__ for %s", discovered.url, exc_info=exc)
            return None

        # Safely navigate Next.js payload
        page_props = (
            data.get("props", {})
                .get("pageProps", {})
        )

        return FetchedPage(
            url=discovered.url,
            source=discovered.source,
            html=resp.text,
            fetched_at=utc_now(),
            metadata=page_props,
        )
