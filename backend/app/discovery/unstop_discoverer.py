import logging
from typing import List
import requests

from app.discovery.base_discoverer import BaseDiscoverer
from app.discovery.discovered_url import DiscoveredURL
from app.domain.event_source import EventSource
from app.utils.time import utc_now

LOG = logging.getLogger("UnstopDiscoverer")


class UnstopDiscoverer(BaseDiscoverer):
    """
    Discovers Unstop hackathons via internal search API.
    """

    SEARCH_API = "https://unstop.com/api/public/search/opportunities"

    def discover(self) -> List[DiscoveredURL]:
        LOG.info("Discovering Unstop hackathons via search API")

        payload = {
            "opportunityType": ["hackathon"],
            "page": 1,
            "perPage": 50,
            "searchTerm": "",
            "filters": {},
        }

        try:
            resp = requests.post(
                self.SEARCH_API,
                json=payload,
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "application/json",
                },
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            LOG.error("Unstop discovery failed", exc_info=exc)
            return []

        items = data.get("data", {}).get("data", [])
        discovered: list[DiscoveredURL] = []

        for item in items:
            slug = item.get("seo_url")
            if not slug:
                continue

            url = f"https://unstop.com/{slug}"

            discovered.append(
                DiscoveredURL(
                    url=url,
                    source=EventSource.UNSTOP,
                    discovered_at=utc_now(),
                )
            )

        LOG.info("Discovered %d Unstop URLs", len(discovered))
        return discovered
