import re
from bs4 import BeautifulSoup

from app.domain.entities.event import Event
from app.domain.entities.fetched_page import FetchedPage

def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def _section_text_after_heading(soup: BeautifulSoup, heading_regex: str) -> str | None:
    h = soup.find(["h1", "h2", "h3", "h4"], string=re.compile(heading_regex, re.I))
    if not h:
        return None
    parts = []
    node = h.find_next_sibling()
    # collect until next heading
    while node and node.name not in ["h1", "h2", "h3", "h4"]:
        parts.append(node.get_text(" ", strip=True))
        node = node.find_next_sibling()
    txt = _clean(" ".join(parts))
    return txt or None

def extract_event(page: FetchedPage) -> Event:
    soup = BeautifulSoup(page.html, "html.parser")

    title_tag = soup.select_one("h1") or soup.select_one("title")
    title = title_tag.get_text(strip=True) if title_tag else page.url

    raw_text = soup.get_text(" ", strip=True)

    description = _section_text_after_heading(soup, r"(about|overview|description)")
    rules = _section_text_after_heading(soup, r"(rules|guidelines)")
    problem = _section_text_after_heading(soup, r"(problem statement|problem statements)")

    # Lightweight heuristics from full text (you’ll refine after seeing real pages)
    registration_deadline = None
    if "Last date" in raw_text or "Deadline" in raw_text:
        # keep it simple for now; refine once you paste a sample HTML snippet
        registration_deadline = None

    return Event(
        title=title,
        url=page.url,
        source=page.source,
        description=description,
        rules=rules,
        problem_statements=[problem] if problem else [],
        raw_text=raw_text[:20000],  # cap it
    )
