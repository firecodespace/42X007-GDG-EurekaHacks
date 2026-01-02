import logging
from pathlib import Path
from typing import List, Set
from urllib.parse import urljoin

from playwright.sync_api import TimeoutError as PWTimeoutError
from playwright.sync_api import sync_playwright

from app.domain.entities.discovered_url import DiscoveredURL
from app.domain.value_objects.event_source import EventSource
from app.shared.utils.time import utc_now

LOG = logging.getLogger("UnstopDiscoverer")

# Absolute, deterministic debug path:
# .../backend/app/adapters/discovery/unstop_discoverer.py -> parents[2] == .../backend/app
DEBUG_DIR = Path(__file__).resolve().parents[2] / "dev" / "debug"


class UnstopDiscoverer:
    LISTING_URL = "https://unstop.com/hackathons"

    def __init__(self, max_scrolls: int = 12):
        self.max_scrolls = max_scrolls

    def discover(self) -> List[DiscoveredURL]:
        found: Set[str] = set()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=120)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            page.on("console", lambda msg: LOG.info("BROWSER_CONSOLE: %s", msg.text))

            page.goto(self.LISTING_URL, wait_until="domcontentloaded", timeout=60000)

            # Wait for at least one hackathon link to exist
            try:
                page.wait_for_selector('a[href*="/hackathons/"]', timeout=20000)
            except PWTimeoutError:
                DEBUG_DIR.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(DEBUG_DIR / "unstop_timeout.png"), full_page=True)
                (DEBUG_DIR / "unstop_timeout.html").write_text(page.content(), encoding="utf-8")
                page.wait_for_timeout(15000)
                context.close()
                browser.close()
                return []

            LOG.info("At URL=%s title=%s", page.url, page.title())

            # Try dismiss overlays (non-fatal)
            for sel in [
                "button:has-text('Accept')",
                "button:has-text('I Agree')",
                "button:has-text('Got it')",
                "button:has-text('Accept All')",
            ]:
                try:
                    page.locator(sel).first.click(timeout=1200)
                    break
                except Exception:
                    pass

            # Progressive scroll: stop if link count stops growing
            last_count = -1
            for _ in range(self.max_scrolls):
                anchors = page.locator('a[href*="/hackathons/"]')
                current = anchors.count()
                if current == last_count:
                    break
                last_count = current
                page.mouse.wheel(0, 8000)
                page.wait_for_timeout(1200)

            anchors = page.locator('a[href*="/hackathons/"]')
            count = anchors.count()
            LOG.info("Unstop rendered hackathon anchors=%s", count)

            # Extract URLs
            for i in range(count):
                href = anchors.nth(i).get_attribute("href")
                if not href:
                    continue
                full = urljoin("https://unstop.com", href.split("?")[0])
                if "/hackathons/" in full and full != self.LISTING_URL:
                    found.add(full)

            # Dump evidence if still empty
            if not found:
                DEBUG_DIR.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(DEBUG_DIR / "unstop_zero.png"), full_page=True)
                (DEBUG_DIR / "unstop_zero.html").write_text(page.content(), encoding="utf-8")
                page.wait_for_timeout(15000)

            context.close()
            browser.close()

        out = [
            DiscoveredURL(url=u, source=EventSource.UNSTOP, discovered_at=utc_now())
            for u in sorted(found)
        ]
        LOG.info("Discovered %d Unstop URLs via Playwright (headed)", len(out))
        return out
