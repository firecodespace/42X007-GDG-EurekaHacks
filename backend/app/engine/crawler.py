# backend/app/engine/crawler.py
import time
import random
import logging
from collections import deque
from typing import List, Optional, Tuple, Dict
from urllib.parse import urlparse, urljoin

from app.engine.registry import get_scraper_for_url
from app.utils.robots import is_allowed

LOG = logging.getLogger("crawler")
LOG.setLevel(logging.INFO)


class Crawler:
    """
    Lightweight crawler.
    Use:
        crawler = Crawler(delay=0.5)
        results = crawler.crawl(start_url, allowed_domains=["mlh.io"], max_pages=100)
    Returns list of data objects returned by scrapers.
    """

    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.domain_last_request = {}

    def _domain_allowed(self, url: str, allowed_domains: Optional[List[str]]) -> bool:
        if not allowed_domains:
            return True
        host = urlparse(url).netloc.lower()
        return any(host == d or host.endswith("." + d) for d in allowed_domains)

    def _throttle(self, url: str):
        host = urlparse(url).netloc.lower()
        last = self.domain_last_request.get(host, 0)
        wait = max(0, self.delay + random.uniform(0.1, 0.3) - (time.time() - last))
        if wait > 0:
            time.sleep(wait)
        self.domain_last_request[host] = time.time()

    def crawl(
        self,
        start_url: str,
        allowed_domains: Optional[List[str]] = None,
        max_pages: int = 100
    ) -> List[Dict]:
        """
        Crawl starting from `start_url`. Returns list of scraped data dicts.
        """
        LOG.info(f"[Crawler] Starting crawl: {start_url}")
        queue = deque([start_url])
        visited = set()
        results: List[Dict] = []
        count = 0

        while queue and count < max_pages:
            url = queue.popleft()

            if url in visited:
                continue

            if not self._domain_allowed(url, allowed_domains):
                LOG.debug(f"[Crawler] Skipping (domain not allowed): {url}")
                visited.add(url)
                continue

            if not is_allowed(url):
                LOG.info(f"[Crawler] Blocked by robots.txt: {url}")
                visited.add(url)
                continue

            scraper = get_scraper_for_url(url)
            if not scraper:
                LOG.debug(f"[Crawler] No scraper registered for URL: {url}")
                visited.add(url)
                continue

            self._throttle(url)

            try:
                data, links = scraper.crawl(url)
            except Exception as e:
                LOG.exception(f"[Crawler] Scraper error for {url}: {e}")
                data, links = None, []

            if data:
                results.append(data)

            visited.add(url)

            # enqueue discovered links (make absolute)
            for l in links or []:
                abs_url = urljoin(url, l)
                if abs_url not in visited:
                    queue.append(abs_url)

            count += 1

        LOG.info(f"[Crawler] Finished. Collected: {len(results)} events (visited {len(visited)} pages)")
        return results
