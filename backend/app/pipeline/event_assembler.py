# app/pipeline/event_assembler.py

from app.extractors.title_extractor import extract_title
from app.extractors.description_extractor import extract_description
from app.extractors.date_extractor import extract_deadline
from app.extractors.location_extractor import extract_location
from app.intelligence.confidence_engine import compute_confidence
from app.ingestion.clean_engine import clean


def assemble_event(
    url: str,
    source: str,
    html: str
) -> dict:
    """
    Converts raw HTML → structured event dict
    """

    cleaned_text = clean(html)

    event = {
        "title": extract_title(html),
        "link": url,
        "source": source,
        "location": extract_location(cleaned_text),
        "deadline": extract_deadline(cleaned_text),
        "raw_description": extract_description(html),
    }

    event["confidence"] = compute_confidence(event)
    return event
