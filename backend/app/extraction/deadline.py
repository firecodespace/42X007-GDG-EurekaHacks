from htmldate import find_date


def extract_deadline_text(text: str) -> str:
    if not text:
        return ""

    try:
        detected = find_date(text)
        return detected or ""
    except Exception:
        return ""
