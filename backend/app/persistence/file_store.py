import json
from pathlib import Path
from datetime import datetime

BASE = Path("backend/data/raw")


def save_events(source: str, events: list):
    date = datetime.utcnow().strftime("%Y-%m-%d")
    path = BASE / source / date
    path.mkdir(parents=True, exist_ok=True)

    events_path = path / "events.json"
    meta_path = path / "metadata.json"

    with open(events_path, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "source": source,
            "date": date,
            "count": len(events)
        }, f, indent=2)
