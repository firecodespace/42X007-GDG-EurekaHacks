import json
from app.scrapers.devpost_scraper import scrape_devpost_events
from app.services.fire_service import save_events_to_firestore

def main():
    events = scrape_devpost_events(limit=50)
    print(f"Scraped {len(events)} events.")
    print(json.dumps(events[:3], indent=2))

    save_events_to_firestore(events)

if __name__ == "__main__":
    main()
