import json
from pathlib import Path

from app.extractors.event_extractor import extract_event


# Point to REAL harvested data
RAW_EVENT_JSON = Path("data/raw/devpost_latest.json")
OUTPUT_JSON = Path("data/test/extracted_event.json")


def main():
    if not RAW_EVENT_JSON.exists():
        raise FileNotFoundError(
            f"Missing input file: {RAW_EVENT_JSON}\n"
            "Run a harvest first."
        )

    raw = json.loads(RAW_EVENT_JSON.read_text(encoding="utf-8"))

    html = raw["html"]
    url = raw.get("url", "unknown")

    event = extract_event(html, source="Devpost", url=url)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(event, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("Event extraction successful")
    print(f"Output written to: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
