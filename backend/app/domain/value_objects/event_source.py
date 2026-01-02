from enum import Enum

class EventSource(str, Enum):
    UNSTOP = "unstop"
    DEVPOST = "devpost"
    HACK2SKILL = "hack2skill"
    DEVFOLIO = "devfolio"
    DEVNOVATE = "devnovate"
    OTHER = "other"