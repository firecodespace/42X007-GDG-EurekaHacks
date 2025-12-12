def normalize_event(event):
    return {
        "title": event.get("title"),
        "link": event.get("link"),
        "source": event.get("source"),
        "location": event.get("location"),
        "deadline": event.get("deadline"),
        "raw_description": event.get("description"),
    }
