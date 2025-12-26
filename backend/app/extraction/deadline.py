import re
from typing import Optional
from dateutil import parser


DATE_PATTERN = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}",
    re.IGNORECASE,
)


def extract_deadline_text(text: str) -> Optional[str]:
    """
    Extract deadline-like date text from plain text.
    This function is heuristic and HTML-agnostic.
    """
    if not text:
        return None

    matches = DATE_PATTERN.findall(text)
    if not matches:
        return None

    # Try parsing full text to get the best date
    try:
        dt = parser.parse(text, fuzzy=True)
        return dt.isoformat()
    except Exception:
        return None
