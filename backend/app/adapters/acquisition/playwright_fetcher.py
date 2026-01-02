import logging
from typing import Optional, Dict, Any

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

from app.acquisition.fetched_page import FetchedPage
from app.discovery.discovered_url import DiscoveredURL
from app.utils.time import utc_now

LOG = logging.getLogger("JSFetcher")


class JSFetcher:
    """
    Fetches fully rendered HTML + API metadata for JS-heavy platforms (Devpost).
    """

    def fetch(self, discovered: DiscoveredURL) -> Optional[FetchedPage]:
        event_metadata: Dict[str, Any] = {}

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                storage_state="storage_state.json",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = context.new_page()

            def extract_challenge(obj):
                """
                Recursively search for Devpost 'challenge' object in GraphQL response.
                """
                if isinstance(obj, dict):
                    if "challenge" in obj and isinstance(obj["challenge"], dict):
                        return obj["challenge"]

                    for value in obj.values():
                        result = extract_challenge(value)
                        if result:
                            return result

                elif isinstance(obj, list):
                    for item in obj:
                        result = extract_challenge(item)
                        if result:
                            return result

                return None


            def handle_response(response):
                try:
                    ct = response.headers.get("content-type", "")
                    if "application/json" not in ct:
                        return

                    url = response.url.lower()
                    if "graphql" not in url:
                        return

                    data = response.json()
                    challenge = extract_challenge(data)

                    if challenge:
                        event_metadata.update(challenge)

                except Exception:
                    pass


            page.on("response", handle_response)

            try:
                page.goto(discovered.url, timeout=60000)
                page.wait_for_load_state("networkidle", timeout=60000)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                page.wait_for_timeout(3000)

                page.evaluate("window.scrollTo(0, 0);")
                page.wait_for_timeout(3000)

                page.wait_for_load_state("networkidle", timeout=60000)

                html = page.content()

                LOG.warning(
                    "Devpost metadata keys for %s: %s",
                    discovered.url,
                    list(event_metadata.keys())[:10],
                )

                return FetchedPage(
                    url=discovered.url,
                    source=discovered.source,
                    html=html,
                    fetched_at=utc_now(),
                    metadata=event_metadata or None,
                )

            except PlaywrightTimeout:
                LOG.error("JS fetch timeout for %s", discovered.url)
                return None

            finally:
                browser.close()
