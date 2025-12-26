from dataclasses import dataclass
from typing import Optional
from app.domain.event_source import EventSource


@dataclass(frozen=True)
class RawEvent:
    """
    Output of deterministic extraction.
    This is NOT the canonical Event yet.
    """
    title: str
    description: str
    deadline_text: Optional[str]
    location_text: Optional[str]

    source: EventSource
    url: str
