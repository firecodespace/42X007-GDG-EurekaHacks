import hashlib


def generate_event_id(source: str, url: str) -> str:
    """
    Deterministic ID so the same event
    always resolves to the same identifier.
    """
    raw = f"{source}:{url}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
