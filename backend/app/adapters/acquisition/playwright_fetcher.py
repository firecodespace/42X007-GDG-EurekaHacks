from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

from app.domain.entities.discovered_url import DiscoveredURL
from app.domain.entities.fetched_page import FetchedPage


DEBUG_DIR = Path(__file__).resolve().parents[2] / "dev" / "debug"


class PlaywrightFetcher:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def fetch(self, discovered: DiscoveredURL) -> Optional[FetchedPage]:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            page.goto(discovered.url, wait_until="domcontentloaded", timeout=60000)

            # Wait for an H1 (event title) to appear
            try:
                page.wait_for_selector("h1", timeout=20000)
            except PWTimeoutError:
                pass

            # Small extra wait for JS hydration
            page.wait_for_timeout(4000)

            title = page.title()
            html = page.content()

            # If title is still the generic Unstop tagline, dump debug artifacts
            if title.startswith("Unstop - Competitions"):
                DEBUG_DIR.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(DEBUG_DIR / "detail_bad.png"), full_page=True)
                (DEBUG_DIR / "detail_bad.html").write_text(html, encoding="utf-8")

            context.close()
            browser.close()

        return FetchedPage(
            url=discovered.url,
            source=discovered.source,
            html=html,
            fetched_at=datetime.now(timezone.utc),
            metadata={
                "fetcher": "playwright",
                "headless": self.headless,
                "page_title": title,
            },
        )
