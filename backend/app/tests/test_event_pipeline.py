from pathlib import Path
from app.pipeline.event_pipeline import build_events

def load_html(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def main():
    html = load_html("public/mock/mlh_event_sample.html")

    pages = [html]

    events = build_events(
        pages=pages,
        source="MLH",
        url="https://events.mlh.io/events/11296"
    )

    print("\n===== EXTRACTED EVENTS =====\n")

    print(f"Total events extracted: {len(events)}\n")

    for i, event in enumerate(events, 1):
        print(f"--- EVENT {i} ---")
        for k, v in event.items():
            if isinstance(v, str) and len(v) > 300:
                print(f"{k}: ({len(v)} chars)")
                print(v)
            else:
                print(f"{k}: {v}")
        print()

if __name__ == "__main__":
    main()
