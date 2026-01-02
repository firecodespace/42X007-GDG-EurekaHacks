from typing import List

from app.adapters.acquisition.http_fetcher import HttpFetcher
from app.adapters.extraction.extract_event import extract_event
from app.domain.entities.event import Event


class EventIngestionPipeline:
    def __init__(self, discoverer, max_events: int = 100):
        self.discoverer = discoverer
        self.max_events = max_events
        self.http_fetcher = HttpFetcher()

    def run(self) -> List[Event]:
        events: List[Event] = []
        discovered = self.discoverer.discover()

        for d in discovered:
            if len(events) >= self.max_events:
                break

            page = self.http_fetcher.fetch(d)
            if not page:
                continue

            ev = extract_event(page)
            events.append(ev)

        return events
