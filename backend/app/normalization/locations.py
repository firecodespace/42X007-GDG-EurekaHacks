from typing import Optional


def normalize_location(location_text: Optional[str]) -> Optional[str]:
    """
    Normalize location into known buckets.
    """
    if not location_text:
        return None

    text = location_text.strip().lower()

    if text in {"online", "virtual"}:
        return "Online"

    if text in {"in-person", "onsite", "on-site"}:
        return "In-Person"

    if text == "hybrid":
        return "Hybrid"

    return location_text.strip()
