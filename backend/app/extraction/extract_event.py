from app.acquisition.fetched_page import FetchedPage
from app.extractors.title_extractor import extract_title
from app.extractors.description_extractor import extract_description
from app.extractors.date_extractor import extract_deadline
from app.extractors.location_extractor import extract_location
from app.domain.raw_event import RawEvent


def extract_event(page: FetchedPage) -> RawEvent:
    """
    Metadata-first extraction.
    API metadata → fallback to HTML.
    """

    meta = page.metadata or {}

    title = meta.get("title") or meta.get("name") or extract_title(page.html)

    description = (
        meta.get("description")
        or meta.get("overview")
        or extract_description(page.html)
    )

    deadline_text = (
        meta.get("submission_deadline")
        or meta.get("deadline")
        or extract_deadline(description)
    )

    location_text = (
        meta.get("location")
        or extract_location(description)
    )

    return RawEvent(
        title=title or "",
        description=description or "",
        deadline_text=deadline_text,
        location_text=location_text,
        source=page.source,
        url=page.url,
    )
