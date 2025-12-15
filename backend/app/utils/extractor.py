from bs4 import BeautifulSoup
import re

STOPWORDS = [
    "log in", "sign up", "register", "cookie", "privacy",
    "terms", "sponsor", "apply", "submit", "dashboard"
]

DESCRIPTION_KEYWORDS = [
    "about", "overview", "description", "details",
    "what is", "why", "who should", "event", "hackathon"
]


def safe_text(node):
    if not node:
        return ""
    return " ".join(node.get_text(" ", strip=True).split())


def score_block(text: str) -> int:
    """Score text block by semantic relevance"""
    score = 0
    t = text.lower()

    # Length matters
    if len(text) > 150:
        score += 2
    if len(text) > 400:
        score += 4

    # Semantic hints
    for kw in DESCRIPTION_KEYWORDS:
        if kw in t:
            score += 3

    # Penalize junk
    for bad in STOPWORDS:
        if bad in t:
            score -= 5

    # Penalize forms
    if "required" in t or "username" in t or "email" in t:
        score -= 6

    return score


def extract_event_data(html: str, url: str, source: str):
    soup = BeautifulSoup(html, "html.parser")

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------
    title = safe_text(soup.find("h1")) or safe_text(soup.find("h2"))

    # --------------------------------------------------
    # FULL VISIBLE TEXT (for pattern mining)
    # --------------------------------------------------
    full_text = safe_text(soup.find("main")) or safe_text(soup)

    # --------------------------------------------------
    # DATE / DEADLINE
    # --------------------------------------------------
    date_pattern = r"[A-Za-z]+\s+[A-Za-z]+\s+\d{1,2},\s+\d{4}.*?(AM|PM).*?(EST|PST|GMT)?"
    date_match = re.search(date_pattern, full_text)

    deadline = date_match.group(0) if date_match else ""

    # --------------------------------------------------
    # LOCATION
    # --------------------------------------------------
    location = "Online" if "hosted online" in full_text.lower() else ""

    if not location:
        loc_match = re.search(r"(location|where)[:\s]+(.+)", full_text, re.I)
        if loc_match:
            location = loc_match.group(2).strip()

    # --------------------------------------------------
    # DESCRIPTION (Semantic Aggregation)
    # --------------------------------------------------
    candidates = []

    for tag in soup.find_all(["p", "div", "section", "article"]):
        text = safe_text(tag)
        if len(text) < 80:
            continue
        score = score_block(text)
        if score > 0:
            candidates.append((score, text))

    candidates.sort(reverse=True, key=lambda x: x[0])

    description = " ".join(text for _, text in candidates[:3])

    # Fallback
    if not description:
        description = full_text[:800]

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------
    return {
        "title": title,
        "link": url,
        "source": source,
        "location": location,
        "deadline": deadline,
        "raw_description": description,
        "confidence": {
            "description_blocks": len(candidates),
            "top_score": candidates[0][0] if candidates else 0
        }
    }
