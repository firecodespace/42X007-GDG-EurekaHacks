# app/engine/crawler.py

from collections import deque
from urllib.parse import urljoin, urlparse

from app.intelligence.link_scoring import score_link
from app.ingestion.fetch_engine import fetch
from app.ingestion.render_engine import render

class Crawler:
    def __init__(self, seeds, allowed_domains, max_pages=200):
        self.queue = deque(seeds)
        self.visited = set()
        self.allowed_domains = allowed_domains
        self.max_pages = max_pages

    def allowed(self, url):
        host = urlparse(url).netloc
        return any(host.endswith(d) for d in self.allowed_domains)

    def run(self):
        pages = {}

        while self.queue and len(pages) < self.max_pages:
            url = self.queue.popleft()
            if url in self.visited or not self.allowed(url):
                continue

            self.visited.add(url)

            html = fetch(url)
            if not html:
                html = render(url)

            if not html:
                continue

            pages[url] = html

            # discover new links
            for part in html.split("href=\""):
                link = part.split("\"")[0]
                if link.startswith("http"):
                    score = score_link(link)
                    if score > 0:
                        self.queue.append(link)

        return pages
