from app.schemas.event import Event
from app.models.event import Event
from app.processors.html_cleaner import clean_html
from app.processors.content_extractor import extract_main_content
from app.processors.sectionizer import split_sections
from app.processors.metadata_extractor import extract_title


def extract_event(html: str, url: str, source: str) -> Event:
    soup = clean_html(html)

    raw_text = extract_main_content(soup)
    sections = split_sections(raw_text)

    title = extract_title(soup)

    return Event(
        source=source,
        url=url,
        title=title,
        description=sections.get("overview"),
        start_date=None,
        end_date=None,
        organizer=None,
        location=None,
        rules=sections.get("rules"),
        prizes=sections.get("prizes"),
        raw_text=raw_text,
        sections=sections
    )
