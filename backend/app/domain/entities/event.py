from dataclasses import dataclass
from typing import Optional

from app.domain.value_objects.event_source import EventSource


@dataclass
class Event:
    title: str
    url: str
    source: EventSource
    description: Optional[str] = None
