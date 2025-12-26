from app.utils.logger import setup_logging
from app.discovery.devpost_discoverer import DevpostDiscoverer
from app.pipeline.event_ingestion import EventIngestionPipeline


def main():
    setup_logging()

    discoverer = DevpostDiscoverer()
    pipeline = EventIngestionPipeline(
        discoverer=discoverer,
        max_events=50,   # change to 100–200 when confident
    )

    events = pipeline.run()

    print("\nFINAL EVENTS:\n")
    for e in events:
        print("-", e.title, "|", e.url)


if __name__ == "__main__":
    main()
