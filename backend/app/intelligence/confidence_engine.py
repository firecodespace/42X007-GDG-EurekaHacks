# app/intelligence/confidence_engine.py

def compute_confidence(event: dict) -> float:
    score = 0

    if event.get("title"):
        score += 0.2
    if event.get("raw_description") and len(event["raw_description"]) > 500:
        score += 0.35
    if event.get("deadline"):
        score += 0.25
    if event.get("location"):
        score += 0.2

    return round(min(score, 1.0), 2)
