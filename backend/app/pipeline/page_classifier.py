# app/pipeline/page_classifier.py

KEYWORDS = [
    "hackathon", "competition", "event",
    "register", "submission", "deadline"
]

def is_event_page(text: str) -> bool:
    score = 0
    t = text.lower()

    for k in KEYWORDS:
        if k in t:
            score += 1

    return score >= 2
