# backend/app/utils/cleaner.py
def normalize_event(event: dict) -> dict:
    """
    Convert raw event into normalized schema used across the system.
    Keep fields stable: title, link, source, location, deadline, raw_description
    """
    normalized = {
        "title": event.get("title") or "",
        "link": event.get("link") or "",
        "source": event.get("source") or "GDG",
        "location": event.get("location") or "",
        "deadline": event.get("date") or "",
        "raw_description": event.get("description") or "",
    }
    return normalized
