import json
from pathlib import Path

from app.extractors.event_extractor import extract_event


HTML_FILE = Path("data/test/devpost_sample.html")
OUTPUT_FILE = Path("data/test/output_event.json")


def main():
    html = HTML_FILE.read_text(encoding="utf-8")

    event = extract_event(
        html=html,
        url="https://awspartyrockhackathon.devpost.com",
        source="Devpost"
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(event.__dict__, f, indent=2, ensure_ascii=False)

    print("Extraction complete")
    print(f"Output written to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
