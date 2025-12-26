import logging
from typing import List
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

from app.discovery.base_discoverer import BaseDiscoverer
from app.discovery.discovered_url import DiscoveredURL
from app.domain.event_source import EventSource
from app.utils.time import utc_now

LOG = logging.getLogger("DevpostDiscoverer")


class DevpostDiscoverer(BaseDiscoverer):
    """
    Devpost discovery via network interception (XHR/JSON),
    not DOM scraping.
    """

    BASE_URL = "https://devpost.com/hackathons"

    def discover(self) -> List[DiscoveredURL]:
        LOG.info("Discovering Devpost hackathon URLs via network interception")

        discovered: list[DiscoveredURL] = []
        seen: set[str] = set()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            def handle_response(response):
                try:
                    if "api" not in response.url.lower():
                        return

                    if not response.headers.get("content-type", "").startswith("application/json"):
                        return

                    data = response.json()

                    # Devpost APIs return lists of challenges / hackathons
                    if isinstance(data, dict):
                        items = data.get("challenges") or data.get("hackathons") or []
                    elif isinstance(data, list):
                        items = data
                    else:
                        return

                    for item in items:
                        url = item.get("url") or item.get("challenge_url")
                        if not url:
                            continue

                        parsed = urlparse(url)
                        if not parsed.netloc.endswith(".devpost.com"):
                            continue

                        if url in seen:
                            continue

                        seen.add(url)
                        discovered.append(
                            DiscoveredURL(
                                url=url,
                                source=EventSource.DEVPOST,
                                discovered_at=utc_now(),
                            )
                        )

                except Exception:
                    pass  # silent on purpose; this is best-effort

            page.on("response", handle_response)

            page.goto(self.BASE_URL, timeout=30000)
            page.wait_for_timeout(8000)

            browser.close()

        LOG.info("Discovered %d Devpost hackathon URLs", len(discovered))
        return discovered
