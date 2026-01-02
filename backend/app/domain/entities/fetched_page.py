from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from app.domain.value_objects.event_source import EventSource


@dataclass(frozen=True)
class FetchedPage:
    url: str
    source: EventSource
    html: str
    fetched_at: datetime
    metadata: Optional[Dict[str, Any]] = None
