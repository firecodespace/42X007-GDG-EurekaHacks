import logging
import random
from typing import Optional

import requests

from app.acquisition.fetched_page import FetchedPage
from app.acquisition.rate_limiter import RateLimiter
from app.acquisition.user_agents import USER_AGENTS
from app.discovery.discovered_url import DiscoveredURL
from app.utils.time import utc_now

LOG = logging.getLogger("Fetcher")


class Fetcher:
    """
    Fetches HTML for discovered URLs.
    No parsing. No extraction.
    """

    def __init__(
        self,
        timeout_seconds: int = 20,
        min_interval_seconds: float = 2.0,
        max_retries: int = 2,
    ):
        self.timeout = timeout_seconds
        self.retries = max_retries
        self.rate_limiter = RateLimiter(min_interval_seconds)

    def fetch(self, discovered: DiscoveredURL) -> Optional[FetchedPage]:
        self.rate_limiter.wait(discovered.source.value)

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "en-US,en;q=0.9",
        }

        for attempt in range(1, self.retries + 1):
            try:
                response = requests.get(
                    discovered.url,
                    headers=headers,
                    timeout=self.timeout,
                )
                response.raise_for_status()

                return FetchedPage(
                    url=discovered.url,
                    source=discovered.source,
                    html=response.text,
                    fetched_at=utc_now(),
                )

            except Exception as exc:
                LOG.warning(
                    "Fetch failed (%s/%s) for %s",
                    attempt,
                    self.retries,
                    discovered.url,
                    exc_info=exc,
                )

        LOG.error("Giving up fetching %s", discovered.url)
        return None
