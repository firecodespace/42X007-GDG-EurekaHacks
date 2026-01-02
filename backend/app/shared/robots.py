# app/utils/robots.py

import requests
import urllib.robotparser
from urllib.parse import urlparse

CACHE = {}

def is_allowed(url: str) -> bool:
    """
    Returns True if the crawler is allowed to fetch this URL.
    Cached per domain.
    """
    host = urlparse(url).netloc
    base = f"https://{host}/robots.txt"

    if base not in CACHE:
        rp = urllib.robotparser.RobotFileParser()
        try:
            resp = requests.get(base, timeout=5)
            if resp.status_code == 200:
                rp.parse(resp.text.splitlines())
            else:
                # If robots.txt missing ΓåÆ assume allowed (industry standard)
                CACHE[base] = True
                return True
        except Exception:
            CACHE[base] = True
            return True
        CACHE[base] = rp

    parser = CACHE[base]
    if parser is True:
        return True

    return parser.can_fetch("*", url)
