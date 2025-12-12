# app/engine/registry.py

from urllib.parse import urlparse

from app.scrapers.devpost_scraper import DevpostScraper
from app.scrapers.mlh_scraper import MLHScraper
from app.scrapers.unstop_scraper import UnstopScraper

# FULL DOMAIN MAPPING
SCRAPER_MAP = {
    "devpost.com": DevpostScraper(),
    ".devpost.com": DevpostScraper(),

    "mlh.io": MLHScraper(),
    ".mlh.io": MLHScraper(),

    "unstop.com": UnstopScraper(),
    ".unstop.com": UnstopScraper(),
}


def get_scraper_for_url(url: str):
    """
    Return scraper instance for given URL, matching exact domain or subdomains.
    """
    host = urlparse(url).netloc.lower()

    for key, scraper in SCRAPER_MAP.items():
        if key.startswith("."):
            # handles *.devpost.com / *.mlh.io / *.unstop.com
            domain = key[1:]
            if host == domain or host.endswith("." + domain):
                return scraper
        else:
            # direct match
            if host == key or host.endswith("." + key):
                return scraper

    return None
