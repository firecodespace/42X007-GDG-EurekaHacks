from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    """User profile for personalized recommendations"""
    
    user_id: str
    skills: List[str] = []  # e.g., ["Python", "React", "ML"]
    work_experience: List[dict] = []  # [{"role": "SWE", "company": "X", "years": 2}]
    events_attended: List[dict] = []  # [{"event_id": "...", "name": "...", "date": "..."}]
    projects: List[dict] = []  # [{"name": "...", "tech": [...], "description": "..."}]
    interests: List[str] = []  # ["AI/ML", "Web3", "IoT"]
    experience_level: str = "intermediate"  # beginner, intermediate, advanced
    preferred_domains: List[str] = []  # ["Healthcare", "Finance", "EdTech"]
    location: Optional[str] = None
    university: Optional[str] = None
