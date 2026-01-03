from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class EventMode(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    HYBRID = "hybrid"


class DeadlineType(str, Enum):
    REGISTRATION = "registration"
    SUBMISSION = "submission"
    EVENT_START = "event_start"
    EVENT_END = "event_end"


class Deadline(BaseModel):
    type: DeadlineType
    date: datetime
    label: Optional[str] = None


class TeamSize(BaseModel):
    min: int = 1
    max: Optional[int] = None


class Organizer(BaseModel):
    name: str
    website: Optional[str] = None
    email: Optional[str] = None
    logo: Optional[str] = None


class ExternalLinks(BaseModel):
    website: Optional[str] = None
    registration: Optional[str] = None
    whatsapp: Optional[str] = None
    discord: Optional[str] = None
    telegram: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    instagram: Optional[str] = None


class Event(BaseModel):
    id: Optional[str] = None
    
    title: str
    description: str
    
    deadlines: List[Deadline] = []
    
    mode: EventMode
    location: Optional[str] = None
    
    organizer: Organizer
    
    prizes: List[str] = []
    
    team_size: TeamSize = TeamSize(min=1, max=4)
    
    eligibility: Optional[str] = None
    rules: List[str] = []
    problem_statements: List[str] = []
    
    external_links: ExternalLinks = ExternalLinks()
    
    source_url: str
    source_platform: str
    
    confidence_score: float = Field(ge=0.0, le=1.0, default=0.0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    raw_data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True


class EventCreate(BaseModel):
    """Schema for creating new events"""
    title: str
    description: str
    source_url: str
    source_platform: str
    raw_data: Optional[Dict[str, Any]] = None


class EventUpdate(BaseModel):
    """Schema for updating events"""
    title: Optional[str] = None
    description: Optional[str] = None
    deadlines: Optional[List[Deadline]] = None
    mode: Optional[EventMode] = None
    location: Optional[str] = None
    prizes: Optional[List[str]] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class EventResponse(BaseModel):
    """API response schema"""
    id: str
    title: str
    description: str
    mode: EventMode
    location: Optional[str]
    organizer: Organizer
    deadlines: List[Deadline]
    prizes: List[str]
    external_links: ExternalLinks
    source_platform: str
    confidence_score: float
    created_at: datetime
