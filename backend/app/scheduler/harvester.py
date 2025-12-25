# app/scheduler/harvester.py

import time
from app.engine.crawler import Crawler
from app.registry.sources import ALL_SOURCES
from app.storage.event_writer import write_events


def run_forever(interval_minutes: int = 60):
    crawler = Crawler(
        seeds=[src["seed"] for src in ALL_SOURCES],
        allowed_domains=[src["domain"] for src in ALL_SOURCES],
        max_pages=500,
        delay=0.5,
    )

    while True:
        print("[HARVESTER] Crawling cycle started")

        events = crawler.run()

        write_events(events)

        print(f"[HARVESTER] Sleeping {interval_minutes} minutes")
        time.sleep(interval_minutes * 60)
