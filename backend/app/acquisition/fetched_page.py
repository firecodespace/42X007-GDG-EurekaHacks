from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from app.domain.event_source import EventSource


@dataclass
class FetchedPage:
    url: str
    source: EventSource
    html: str
    fetched_at: datetime
    metadata: Optional[Dict[str, Any]] = None
