from typing import List

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

from app.adapters.acquisition.http_fetcher import HttpFetcher
from app.adapters.extraction.extract_event import extract_event
from app.domain.entities.event import Event
from app.domain.entities.fetched_page import FetchedPage
from app.domain.value_objects.event_source import EventSource
from datetime import datetime, timezone


class EventIngestionPipeline:
    def __init__(self, discoverer, max_events: int = 100):
        self.discoverer = discoverer
        self.max_events = max_events
        self.http_fetcher = HttpFetcher()

    def run(self) -> List[Event]:
        events: List[Event] = []
        discovered = self.discoverer.discover()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(ignore_https_errors=True)

            for d in discovered:
                if len(events) >= self.max_events:
                    break

                # Use Playwright only for Unstop
                if d.source == EventSource.UNSTOP:
                    page = context.new_page()
                    try:
                        page.goto(d.url, wait_until="domcontentloaded", timeout=60000)
                        try:
                            page.wait_for_selector("h1", timeout=15000)
                        except PWTimeoutError:
                            pass
                        html = page.content()
                    finally:
                        page.close()

                    fetched = FetchedPage(
                        url=d.url,
                        source=d.source,
                        html=html,
                        fetched_at=datetime.now(timezone.utc),
                        metadata={"fetcher": "playwright"},
                    )
                else:
                    fetched = self.http_fetcher.fetch(d)
                    if not fetched:
                        continue

                ev = extract_event(fetched)
                events.append(ev)

            context.close()
            browser.close()

        return events
