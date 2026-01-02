import logging
from typing import List, Set
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from app.domain.entities.discovered_url import DiscoveredURL
from app.domain.value_objects.event_source import EventSource
from app.shared.utils.time import utc_now

LOG = logging.getLogger("UnstopDiscoverer")


class UnstopDiscoverer:
    LISTING_URL = "https://unstop.com/hackathons"

    def __init__(self, max_scrolls: int = 10):
        self.max_scrolls = max_scrolls

    def discover(self) -> List[DiscoveredURL]:
        found: Set[str] = set()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=150)
            page = browser.new_page()

            page.on("console", lambda msg: LOG.info("BROWSER_CONSOLE: %s", msg.text))

            page.goto(self.LISTING_URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(15000)

            LOG.info("At URL=%s title=%s", page.url, page.title())

            # Try to close cookie/consent if it exists (non-fatal)
            for sel in ["button:has-text('Accept')", "button:has-text('I Agree')", "button:has-text('Got it')"]:
                try:
                    page.locator(sel).first.click(timeout=1500)
                    break
                except Exception:
                    pass

            # Scroll
            for _ in range(self.max_scrolls):
                page.mouse.wheel(0, 7000)
                page.wait_for_timeout(1200)

            anchors = page.locator('a[href*="/hackathons/"]')
            count = anchors.count()
            LOG.info("Unstop rendered hackathon anchors=%s", count)

            if count == 0:
                os.makedirs("debug", exist_ok=True)
                page.screenshot(path="debug/unstop_zero.png", full_page=True)
                html = page.content()
                with open("debug/unstop_zero.html", "w", encoding="utf-8") as f:
                    f.write(html)
                # Keep it open so you can see what page it is
                page.wait_for_timeout(15000)

            browser.close()

        out = [DiscoveredURL(url=u, source=EventSource.UNSTOP, discovered_at=utc_now()) for u in sorted(found)]
        LOG.info("Discovered %d Unstop URLs via Playwright (headed)", len(out))
        return out
