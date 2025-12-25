# app/harvest/run.py

from app.engine.crawler import Crawler
from app.registry.sources import ALL_SOURCES
from app.storage.event_writer import write_events


def main():
    print("[HARVEST] Starting batch")

    for src in ALL_SOURCES:
        print(f"[HARVEST] Source: {src['name']}")

        crawler = Crawler(
            seeds=[src["seed"]],                 # ✅ FIX: seeds (plural, list)
            allowed_domains=src["domains"],
            fetch_mode=src.get("fetch_mode", "http"),
            max_pages=src.get("max_pages", 200),
        )

        pages = crawler.run()
        write_events(pages, source=src["name"])

    print("[HARVEST] Done")


if __name__ == "__main__":
    main()
