from app.domain.event import Event


def is_valid_event(event: Event) -> bool:
    title = event.title.lower()
    description = event.description.lower()

    # Hard exclusions
    forbidden_keywords = [
        "sign up", "signup", "log in", "login",
        "register", "account", "privacy",
        "terms", "policy", "about us",
        "contact", "blog", "careers",
        "security", "guidelines",
    ]

    if any(k in title for k in forbidden_keywords):
        return False

    # Positive signals of a real event
    positive_signals = [
        "hackathon",
        "challenge",
        "competition",
        "prize",
        "submission",
        "deadline",
        "build",
        "win",
    ]

    if not any(s in title or s in description for s in positive_signals):
        return False

    # Must have a deadline OR strong description
    if event.deadline is None and len(event.description) < 500:
        return False

    return True
