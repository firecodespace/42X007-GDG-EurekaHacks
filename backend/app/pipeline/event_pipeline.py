from app.extractors.event_extractor import extract_event_data


def build_events(pages: list, source: str) -> list:
    results = []

    for page in pages:
        try:
            event = extract_event_data(
                html=page["html"],
                url=page["url"],
                source=source
            )

            if event.get("raw_description"):
                results.append(event)

        except Exception:
            continue

    return results
