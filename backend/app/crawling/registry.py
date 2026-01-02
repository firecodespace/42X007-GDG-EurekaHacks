from urllib.parse import urlparse

from app.scrapers.mlh_scraper import MLHScraper
from app.scrapers.unstop_scraper import UnstopScraper

# If you have a Devpost scraper class inside run_devpost_scraper.py, we can add it later.
# For now, keep only the sources that exist.

SCRAPER_MAP = {
    "mlh.io": MLHScraper(),
    "unstop.com": UnstopScraper(),
}

def get_scraper_for_url(url: str):
    host = urlparse(url).netloc.lower()
    for domain, scraper in SCRAPER_MAP.items():
        if host == domain or host.endswith("." + domain):
            return scraper
    return None
