from pathlib import Path
import json
from datetime import datetime


BASE_DIR = Path("data")


def write_events(events: list):
    if not events:
        return

    BASE_DIR.mkdir(exist_ok=True)

    grouped = {}

    for event in events:
        source = event.get("source", "unknown").lower()
        grouped.setdefault(source, []).append(event)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    for source, items in grouped.items():
        source_dir = BASE_DIR / source
        source_dir.mkdir(parents=True, exist_ok=True)

        out_file = source_dir / f"events_{timestamp}.json"
        with out_file.open("w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

        print(f"[STORAGE] Saved {len(items)} → {out_file}")
