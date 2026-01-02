import logging
from typing import List

from app.discovery.base_discoverer import BaseDiscoverer
from app.acquisition.fetcher import Fetcher
from app.acquisition.js_fetcher import JSFetcher
from app.acquisition.unstop_fetcher import UnstopFetcher
from app.extraction.extract_event import extract_event
from app.normalization.build_event import build_event
from app.normalization.validators import ValidationError
from app.pipeline.event_filter import is_valid_event
from app.domain.event import Event
from app.domain.event_source import EventSource

LOG = logging.getLogger("EventIngestionPipeline")


class EventIngestionPipeline:
    """
    Orchestrates discovery → fetch → extract → normalize → filter.
    """

    def __init__(
        self,
        discoverer: BaseDiscoverer,
        max_events: int = 100,
    ):
        self.discoverer = discoverer
        self.max_events = max_events

        # Fetchers (source-aware)
        self.fetcher = Fetcher()               # generic / static
        self.js_fetcher = JSFetcher()           # Devpost
        self.unstop_fetcher = UnstopFetcher()   # Unstop (API)

    def run(self) -> List[Event]:
        events: list[Event] = []
        discovered = self.discoverer.discover()

        LOG.info("Discovered %d candidate URLs", len(discovered))

        for discovered_url in discovered:
            if len(events) >= self.max_events:
                LOG.info("Reached max_events=%d, stopping", self.max_events)
                break

            try:
                # -------- SOURCE ROUTING (CRITICAL) --------
                if discovered_url.source == EventSource.UNSTOP:
                    page = self.unstop_fetcher.fetch(discovered_url)

                elif discovered_url.source == EventSource.DEVPOST:
                    page = self.js_fetcher.fetch(discovered_url)

                else:
                    page = self.fetcher.fetch(discovered_url)
                # ------------------------------------------

                if not page:
                    continue

                raw = extract_event(page)
                event = build_event(raw)

                if not is_valid_event(event):
                    LOG.info("Filtered non-event page: %s", event.url)
                    continue

                events.append(event)
                LOG.info(
                    "Accepted event (%d/%d): %s",
                    len(events),
                    self.max_events,
                    event.title,
                )

            except ValidationError as ve:
                LOG.warning(
                    "Validation failed for %s: %s",
                    discovered_url.url,
                    ve,
                )

            except Exception as exc:
                LOG.error(
                    "Unexpected failure for %s",
                    discovered_url.url,
                    exc_info=exc,
                )

        LOG.info("Ingestion finished with %d valid events", len(events))
        return events
