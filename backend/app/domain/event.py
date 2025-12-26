from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.event_source import EventSource


@dataclass(frozen=True)
class Event:
    """
    Canonical Event entity.
    This is the single source of truth for what an event is.
    """

    id: str                     # Deterministic hash (url + source)
    title: str
    description: str

    source: EventSource
    url: str

    deadline: Optional[datetime]
    location: Optional[str]     # Online / In-Person / Hybrid / City / Country

    created_at: datetime
    updated_at: datetime
