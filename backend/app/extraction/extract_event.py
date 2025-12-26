from app.acquisition.fetched_page import FetchedPage
from app.extraction.raw_event import RawEvent
from app.extraction.title import extract_title
from app.extraction.description import extract_description
from app.extraction.deadline import extract_deadline_text
from app.extraction.location import extract_location_text


def extract_event(page: FetchedPage) -> RawEvent:
    """
    Deterministically extracts raw event data from HTML snapshot.
    """

    title = extract_title(page.html)
    description = extract_description(page.html)

    combined_text = f"{title}\n{description}"

    deadline_text = extract_deadline_text(combined_text)
    location_text = extract_location_text(combined_text)

    return RawEvent(
        title=title,
        description=description,
        deadline_text=deadline_text or None,
        location_text=location_text or None,
        source=page.source,
        url=page.url,
    )
