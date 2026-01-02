from dataclasses import dataclass, field
from typing import List, Optional, Dict
from app.domain.value_objects.event_source import EventSource

@dataclass
class Event:
    title: str
    url: str
    source: EventSource

    registration_deadline: Optional[str] = None
    timelines: List[str] = field(default_factory=list)

    mode: Optional[str] = None
    team_size: Optional[str] = None
    fees: Optional[str] = None

    prize_pool: Optional[str] = None
    perks: List[str] = field(default_factory=list)

    links: List[str] = field(default_factory=list)

    description: Optional[str] = None
    rules: Optional[str] = None
    problem_statements: List[str] = field(default_factory=list)

    raw_text: Optional[str] = None  # fallback
