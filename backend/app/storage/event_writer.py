# app/storage/event_writer.py

import json
from pathlib import Path
from datetime import datetime
from typing import Dict


BASE_DATA_DIR = Path("data")


def write_events(pages: Dict[str, str], source: str) -> None:
    """
    Persist crawled pages to disk.

    Structure:
        data/
          └── <source>/
                └── raw/
                      └── batch_<timestamp>.json

    pages: {url: html}
    """

    if not pages:
        print(f"[WRITER] No pages to write for {source}")
        return

    # -----------------------------------------
    # Directory setup
    # -----------------------------------------
    source_dir = BASE_DATA_DIR / source.lower()
    raw_dir = source_dir / "raw"

    raw_dir.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------
    # File name
    # -----------------------------------------
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_file = raw_dir / f"batch_{timestamp}.json"

    # -----------------------------------------
    # Serialize
    # -----------------------------------------
    payload = {
        "source": source,
        "timestamp": timestamp,
        "count": len(pages),
        "pages": [
            {
                "url": url,
                "html": html
            }
            for url, html in pages.items()
        ]
    }

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"[WRITER] Saved {len(pages)} pages → {out_file}")
