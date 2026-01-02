from typing import Dict, Any


class Event:
    def __init__(
        self,
        title: str,
        source: str,
        url: str,
        raw_text: str,
        sections: Dict[str, str] | None = None,
        location: str | None = None,
        deadline: str | None = None,
        confidence: float | None = None,
    ):
        self.title = title
        self.source = source
        self.url = url
        self.raw_text = raw_text
        self.sections = sections or {}
        self.location = location
        self.deadline = deadline
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        """
        Canonical JSON-safe representation.
        This is what storage + LLMs will consume.
        """
        return {
            "title": self.title,
            "source": self.source,
            "url": self.url,
            "location": self.location,
            "deadline": self.deadline,
            "confidence": self.confidence,
            "sections": self.sections,
            "raw_text_length": len(self.raw_text) if self.raw_text else 0,
        }
