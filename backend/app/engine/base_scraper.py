# app/engine/base_scraper.py

from typing import Tuple, Dict, List

class BaseScraper:
    """
    Every domain-specific scraper MUST implement:

        crawl(url: str) -> (data, links)

    data  = dict containing extracted competition info OR None
    links = list of URLs discovered on this page that the crawler should visit

    This allows:
        - detail pages to return data
        - list pages to return only links
    """

    def crawl(self, url: str) -> Tuple[Dict, List[str]]:
        raise NotImplementedError("Scraper must implement crawl()")
