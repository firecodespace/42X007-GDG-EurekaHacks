from app.extraction.raw_event import RawEvent


class ValidationError(Exception):
    pass


def validate_raw_event(event: RawEvent) -> None:
    """
    Raise ValidationError if raw event is unusable.
    """

    if not event.title or len(event.title) < 4:
        raise ValidationError("Invalid or missing title")

    if not event.description or len(event.description) < 100:
        raise ValidationError("Description too short")

    if not event.url.startswith("http"):
        raise ValidationError("Invalid URL")

    if not event.source:
        raise ValidationError("Missing source")
