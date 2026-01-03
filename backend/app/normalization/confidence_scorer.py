from typing import Dict, Any
from app.domain.event import Event


class ConfidenceScorer:
    """Calculate confidence score for extracted event data"""
    
    WEIGHTS = {
        "title": 0.15,
        "description": 0.15,
        "deadlines": 0.15,
        "prizes": 0.10,
        "organizer": 0.10,
        "external_links": 0.10,
        "mode": 0.05,
        "location": 0.05,
        "eligibility": 0.05,
        "rules": 0.05,
        "team_size": 0.05,
    }
    
    def calculate_score(self, event: Event) -> float:
        """
        Calculate confidence score based on data completeness
        
        Args:
            event: Event object to score
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        score = 0.0
        
        if event.title and len(event.title) > 5:
            score += self.WEIGHTS["title"]
        
        if event.description and len(event.description) > 50:
            score += self.WEIGHTS["description"]
        
        if event.deadlines and len(event.deadlines) > 0:
            score += self.WEIGHTS["deadlines"]
        
        if event.prizes and len(event.prizes) > 0:
            score += self.WEIGHTS["prizes"]
        
        if event.organizer and event.organizer.name:
            score += self.WEIGHTS["organizer"]
        
        link_count = sum([
            1 for key, value in event.external_links.dict().items()
            if value is not None
        ])
        if link_count > 0:
            score += self.WEIGHTS["external_links"] * min(link_count / 3, 1.0)
        
        if event.mode:
            score += self.WEIGHTS["mode"]
        
        if event.location:
            score += self.WEIGHTS["location"]
        
        if event.eligibility:
            score += self.WEIGHTS["eligibility"]
        
        if event.rules and len(event.rules) > 0:
            score += self.WEIGHTS["rules"]
        
        if event.team_size:
            score += self.WEIGHTS["team_size"]
        
        return min(round(score, 2), 1.0)


confidence_scorer = ConfidenceScorer()
