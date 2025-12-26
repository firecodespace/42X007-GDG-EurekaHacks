from dataclasses import dataclass
from datetime import datetime
from app.domain.event_source import EventSource


@dataclass(frozen=True)
class DiscoveredURL:
    url: str
    source: EventSource
    discovered_at: datetime
