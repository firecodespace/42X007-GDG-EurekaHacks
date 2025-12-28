from app.acquisition.fetched_page import FetchedPage
from app.extractors.title_extractor import extract_title
from app.extractors.description_extractor import extract_description
from app.extractors.date_extractor import extract_deadline
from app.extractors.location_extractor import extract_location
from app.domain.raw_event import RawEvent
from app.domain.event_source import EventSource


def extract_event(page: FetchedPage) -> RawEvent:
    """
    Metadata-first extraction.
    API metadata → fallback to HTML.
    """

    meta = page.metadata or {}

    # ---------- TITLE ----------
    title = (
        meta.get("title")
        or meta.get("name")
        or meta.get("opportunity_name")      # Unstop
        or extract_title(page.html)
    )

    # ---------- DESCRIPTION ----------
    description = (
        meta.get("description")
        or meta.get("about")                 # Unstop
        or meta.get("overview")
        or extract_description(page.html)
    )

    # ---------- DEADLINE ----------
    deadline_text = (
        meta.get("submission_deadline")      # Devpost
        or meta.get("registrationDeadline")  # Unstop
        or meta.get("end_date")
        or meta.get("deadline")
        or extract_deadline(description)
    )

    # ---------- LOCATION / MODE ----------
    location_text = (
        meta.get("location")
        or meta.get("mode")                  # Unstop: Online / Offline
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
