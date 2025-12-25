# app/extractors/location_extractor.py

def extract_location(text: str) -> str:
    t = text.lower()

    ONLINE_PHRASES = [
        "hosted online",
        "event is online",
        "virtual event",
        "online hackathon"
    ]

    IN_PERSON_PHRASES = [
        "in person",
        "on site",
        "on-site",
        "at campus",
        "at university"
    ]

    for p in ONLINE_PHRASES:
        if p in t:
            return "Online"

    for p in IN_PERSON_PHRASES:
        if p in t:
            return "In-Person"

    if "hybrid" in t:
        return "Hybrid"

    return ""
