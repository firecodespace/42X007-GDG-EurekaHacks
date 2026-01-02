from datetime import datetime, timezone
from typing import Optional
import requests

from app.domain.entities.discovered_url import DiscoveredURL
from app.domain.entities.fetched_page import FetchedPage


class HttpFetcher:
    def fetch(self, discovered: DiscoveredURL) -> Optional[FetchedPage]:
        resp = requests.get(
            discovered.url,
            timeout=30,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
        )
        resp.raise_for_status()
        return FetchedPage(
            url=discovered.url,
            source=discovered.source,
            html=resp.text,
            fetched_at=datetime.now(timezone.utc),
            metadata=None,
        )
