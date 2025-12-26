import logging
from datetime import datetime
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.discovery.base_discoverer import BaseDiscoverer
from app.discovery.discovered_url import DiscoveredURL
from app.domain.event_source import EventSource
from app.utils.time import utc_now

LOG = logging.getLogger("DevpostDiscoverer")


class DevpostDiscoverer(BaseDiscoverer):
    """
    Discovers hackathon URLs from Devpost list pages.
    """

    BASE_URL = "https://devpost.com/hackathons"

    def discover(self) -> List[DiscoveredURL]:
        LOG.info("Discovering Devpost hackathon URLs")

        try:
            response = requests.get(
                self.BASE_URL,
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response.raise_for_status()

            LOG.info("Devpost response length: %d", len(response.text))

        except Exception as exc:
            LOG.error("Devpost discovery failed", exc_info=exc)
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        discovered: list[DiscoveredURL] = []
        seen = set()

        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href:
                continue

            if not href.startswith("http"):
                continue

            if any(x in href for x in ["/login", "/signup", "/settings"]):
                continue

            if ".devpost.com" not in href:
                continue

            if href in seen:
                continue

            seen.add(href)

            discovered.append(
                DiscoveredURL(
                    url=href,
                    source=EventSource.DEVPOST,
                    discovered_at=utc_now()
                )
            )

        LOG.info("Discovered %d Devpost URLs", len(discovered))
        return discovered
