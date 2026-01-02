from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.domain.value_objects.event_source import EventSource


@dataclass(frozen=True)
class DiscoveredURL:
    url: str
    source: EventSource
    discovered_at: datetime
    referrer_url: Optional[str] = None
