# app/intelligence/link_scoring.py

IMPORTANT_KEYWORDS = [
    "hack", "event", "challenge", "competition", "register",
    "submit", "deadline"
]

BLOCK_KEYWORDS = [
    "login", "privacy", "terms", "careers", "about", "contact"
]

def score_link(url: str) -> int:
    score = 0
    lower = url.lower()

    for k in IMPORTANT_KEYWORDS:
        if k in lower:
            score += 2

    for k in BLOCK_KEYWORDS:
        if k in lower:
            score -= 3

    return score
