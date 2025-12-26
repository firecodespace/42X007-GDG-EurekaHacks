from dataclasses import dataclass
from typing import Optional
from app.domain.event_source import EventSource


@dataclass
class RawEvent:
    """
    Unvalidated, extracted event data.
    This represents data as it comes from the web (HTML / API).
    """

    title: str
    description: str

    deadline_text: Optional[str]
    location_text: Optional[str]

    source: EventSource
    url: str
