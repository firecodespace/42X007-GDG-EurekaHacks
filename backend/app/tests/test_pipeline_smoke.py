from app.extractors.event_extractor import extract_event_data

def main():
    html = "<html><body><h1>Test Hack</h1><p>This is a test event.</p></body></html>"
    event = extract_event_data(html, "https://example.com", "test")

    print("\n===== PIPELINE TEST =====")
    for k, v in event.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
