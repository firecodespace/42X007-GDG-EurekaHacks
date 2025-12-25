# app/extractors/description_extractor.py

from bs4 import BeautifulSoup

BLACKLIST_KEYWORDS = [
    "schedule", "agenda", "faq", "rules",
    "eligibility", "sponsors", "timeline"
]

def extract_description(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    candidates = soup.find_all(["section", "article", "div", "p"])

    scored = []
    for c in candidates:
        text = c.get_text(" ", strip=True)
        if len(text) < 150:
            continue

        penalty = sum(1 for k in BLACKLIST_KEYWORDS if k in text.lower())
        score = len(text) - (penalty * 200)
        scored.append((score, text))

    if not scored:
        return ""

    scored.sort(reverse=True)
    return scored[0][1]
