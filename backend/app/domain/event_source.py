from enum import Enum

class EventSource(str, Enum):
    DEVPOST = "devpost"
    MLH = "mlh"
    UNSTOP = "unstop"
    HACK2SKILL = "hack2skill"
    OTHER = "other"