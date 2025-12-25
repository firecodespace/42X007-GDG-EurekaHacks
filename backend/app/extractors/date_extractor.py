# app/extractors/date_extractor.py

import re
from htmldate import find_date

DATE_RANGE_PATTERN = (
    r"([A-Z][a-z]+ [A-Z][a-z]+ \d{1,2}, \d{4})"
)

def extract_deadline(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""

    try:
        detected = find_date(text)
        return detected or ""
    except Exception:
        return ""

