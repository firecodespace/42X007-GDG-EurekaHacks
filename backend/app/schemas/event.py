from typing import Optional, List, Dict
from dataclasses import dataclass


@dataclass
class Event:
    source: str
    url: str

    title: Optional[str]
    description: Optional[str]

    start_date: Optional[str]
    end_date: Optional[str]

    organizer: Optional[str]
    location: Optional[str]

    rules: Optional[str]
    prizes: Optional[str]

    raw_text: str
    sections: Dict[str, str]
