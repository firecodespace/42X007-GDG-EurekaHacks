from app.discovery.devpost_discoverer import DevpostDiscoverer
from app.acquisition.fetcher import Fetcher
from app.extraction.extract_event import extract_event
from app.normalization.build_event import build_event


def test_single_event_pipeline():
    """
    Full vertical slice test:
    Discovery → Fetch → Extract → Normalize
    (limited to ONE real event)
    """

    discoverer = DevpostDiscoverer()
    discovered_urls = discoverer.discover()

    assert discovered_urls, "No URLs discovered from Devpost"

    fetcher = Fetcher(min_interval_seconds=2.0)

    page = fetcher.fetch(discovered_urls[0])
    assert page is not None, "Failed to fetch event page"

    raw = extract_event(page)
    event = build_event(raw)

    # Print for manual inspection (allowed in -s mode)
    print("\nFINAL EVENT OBJECT:\n", event)

    assert event.title
    assert event.url
    assert event.source
