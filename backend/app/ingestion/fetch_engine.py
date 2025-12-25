# app/ingestion/fetch_engine.py

import time
import logging
import requests
from requests.adapters import HTTPAdapter, Retry

LOG = logging.getLogger("fetch_engine")

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch(url: str, timeout: int = 15) -> str | None:
    try:
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.4,
            status_forcelist=[403, 429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        session.headers.update(DEFAULT_HEADERS)

        resp = session.get(url, timeout=timeout)
        if resp.status_code != 200:
            return None

        time.sleep(0.2)
        return resp.text

    except Exception as e:
        LOG.warning(f"[fetch_engine] {url} failed: {e}")
        return None
