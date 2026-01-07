from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models.user_profile import UserProfile
from app.persistence.profile_repo import profile_repo
from app.persistence.firestore_repo import firestore_repo
from app.services.personalization_service import personalization_service
from app.shared.logger import logger

router = APIRouter()

@router.post("/feed")
async def get_personalized_feed(
    user_id: str,
    limit: int = 10,
    min_match_score: int = 60
) -> Dict[str, Any]:
    """Generate personalized event feed for user"""
    
    try:
        logger.info(f"[Recommendations] Generating feed for user: {user_id}")
        
        # Get user profile
        profile = await profile_repo.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get latest events
        events = await firestore_repo.list_events(limit=50)
        if not events:
            raise HTTPException(status_code=404, detail="No events available")
        
        logger.info(f"[Recommendations] Processing {len(events)} events...")
        
        # Personalize each
        personalized_events = []
        for event in events:
            try:
                personalized = await personalization_service.personalize_event(
                    event=event,
                    user_profile=profile,
                    use_cache=True
                )
                
                match_score = personalized.get("personalization", {}).get("match_score", 0)
                if match_score >= min_match_score:
                    personalized_events.append(personalized)
                
            except Exception as e:
                logger.warning(f"[Recommendations] Failed: {event.id}: {e}")
                continue
        
        # Sort by match_score
        personalized_events.sort(
            key=lambda x: x.get("personalization", {}).get("match_score", 0),
            reverse=True
        )
        
        final_feed = personalized_events[:limit]
        
        logger.info(f"[Recommendations] ✅ Feed ready: {len(final_feed)} events")
        
        return {
            "success": True,
            "user_id": user_id,
            "total_available": len(personalized_events),
            "recommended": len(final_feed),
            "events": final_feed
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Recommendations] Feed generation failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")
