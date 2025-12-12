# backend/app/scrapers/run_gdg_scraper.py
import logging
import json
from app.scrapers.gdg_scraper import scrape_gdg_events
from app.services.fire_service import save_events_to_firestore

LOG = logging.getLogger("run_gdg_scraper")
logging.basicConfig(level=logging.INFO)

def main():
    events = scrape_gdg_events(limit=50)
    LOG.info("Got %d events", len(events))
    result = save_events_to_firestore(events)
    LOG.info("Save result: %s", result)
    # Also print a short sample
    print(json.dumps(events[:3], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
