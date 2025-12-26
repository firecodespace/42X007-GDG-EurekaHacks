from app.domain.event import Event
from app.extraction.raw_event import RawEvent
from app.normalization.dates import normalize_deadline
from app.normalization.locations import normalize_location
from app.normalization.validators import validate_raw_event
from app.utils.ids import generate_event_id
from app.utils.time import utc_now


def build_event(raw: RawEvent) -> Event:
    """
    Convert RawEvent into canonical Event.
    Raises ValidationError if invalid.
    """

    validate_raw_event(raw)

    deadline = normalize_deadline(raw.deadline_text)
    location = normalize_location(raw.location_text)

    now = utc_now()
    event_id = generate_event_id(raw.source.value, raw.url)

    return Event(
        id=event_id,
        title=raw.title.strip(),
        description=raw.description.strip(),
        source=raw.source,
        url=raw.url,
        deadline=deadline,
        location=location,
        created_at=now,
        updated_at=now,
    )
