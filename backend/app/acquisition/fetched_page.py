from dataclasses import dataclass
from datetime import datetime
from app.domain.event_source import EventSource


@dataclass(frozen=True)
class FetchedPage:
    url: str
    source: EventSource
    html: str
    fetched_at: datetime
