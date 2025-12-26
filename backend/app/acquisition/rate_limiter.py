import time
from collections import defaultdict


class RateLimiter:
    """
    Simple per-source rate limiter.
    """

    def __init__(self, min_interval_seconds: float):
        self.min_interval = min_interval_seconds
        self._last_call = defaultdict(float)

    def wait(self, key: str) -> None:
        now = time.time()
        elapsed = now - self._last_call[key]

        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)

        self._last_call[key] = time.time()
