def extract_location_text(text: str) -> str:
    if not text:
        return ""

    t = text.lower()

    if "hybrid" in t:
        return "Hybrid"

    online_phrases = [
        "hosted online",
        "event is online",
        "virtual event",
        "online hackathon",
    ]

    for p in online_phrases:
        if p in t:
            return "Online"

    in_person_phrases = [
        "in person",
        "on site",
        "on-site",
        "at campus",
        "at university",
    ]

    for p in in_person_phrases:
        if p in t:
            return "In-Person"

    return ""
