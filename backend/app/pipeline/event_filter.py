from app.domain.event import Event


def is_valid_event(event: Event) -> bool:
    """
    Hard quality gate for deciding whether a page
    is a real event or junk (login, signup, marketing).
    """

    forbidden_keywords = [
        "sign up",
        "signup",
        "log in",
        "login",
        "register",
        "account",
        "profile",
    ]

    title = event.title.lower()

    if any(k in title for k in forbidden_keywords):
        return False

    # Must look like a real event
    if event.deadline is None and len(event.description) < 300:
        return False

    return True
