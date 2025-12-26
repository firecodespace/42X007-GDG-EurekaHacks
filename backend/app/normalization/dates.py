from datetime import datetime, timezone
from typing import Optional
from dateutil import parser


def normalize_deadline(deadline_text: Optional[str]) -> Optional[datetime]:
    """
    Convert extracted deadline text to UTC datetime.
    Returns None if parsing fails.
    """
    if not deadline_text:
        return None

    try:
        dt = parser.parse(deadline_text, fuzzy=True)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None
