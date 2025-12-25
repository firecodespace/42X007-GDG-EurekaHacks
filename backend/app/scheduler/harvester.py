import time

from app.engine.crawler import Crawler
from app.registry.sources import ALL_SOURCES
from app.pipeline.event_pipeline import build_events
from app.storage.event_writer import write_events


def run_once():
    print("[HARVESTER] One-time crawl started")

    for source in ALL_SOURCES:
        print(f"[HARVESTER] Crawling source: {source['name']}")

        crawler = Crawler(
            seeds=[source["seed"]],
            allowed_domains=[source["domain"]],
            max_pages=300,
        )

        pages = crawler.run()

        if not pages:
            print(f"[HARVESTER] No pages fetched for {source['name']}")
            continue

        events = build_events(
            pages=list(pages.values()),
            source=source["name"],
        )

        if not events:
            print(f"[HARVESTER] No events extracted for {source['name']}")
            continue

        write_events(events, source["name"])

        print(
            f"[HARVESTER] Saved {len(events)} events for {source['name']}"
        )

    print("[HARVESTER] One-time crawl finished")


def run_forever(interval_minutes: int = 60):
    while True:
        run_once()
        print(f"[HARVESTER] Sleeping {interval_minutes} minutes")
        time.sleep(interval_minutes * 60)
