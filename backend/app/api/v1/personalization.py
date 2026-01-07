from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.models.user_profile import UserProfile
from app.services.personalization_service import personalization_service
from app.persistence.firestore_repo import firestore_repo
from app.shared.logger import logger

router = APIRouter()


@router.post("/personalize/{event_id}")
async def personalize_event(
    event_id: str,
    user_profile: UserProfile
) -> Dict[str, Any]:
    """
    Generate personalized event recommendation
    
    **Input:** User profile JSON
    **Output:** Enhanced event JSON with personalization
    """
    
    try:
        # Fetch event from Firestore
        event = await firestore_repo.get_event(event_id)
        
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Generate personalization
        personalized_event = await personalization_service.personalize_event(
            event=event,
            user_profile=user_profile
        )
        
        return {
            "success": True,
            "event_id": event_id,
            "data": personalized_event
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] Personalization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/personalize/batch")
async def personalize_events_batch(
    event_ids: list[str],
    user_profile: UserProfile
) -> Dict[str, Any]:
    """
    Generate personalized recommendations for multiple events
    
    **Use case:** Homepage feed with top 10 recommended events
    """
    
    try:
        personalized_events = []
        
        for event_id in event_ids:
            event = await firestore_repo.get_event(event_id)
            
            if event:
                personalized = await personalization_service.personalize_event(
                    event=event,
                    user_profile=user_profile
                )
                personalized_events.append(personalized)
        
        # Sort by match_score
        personalized_events.sort(
            key=lambda x: x.get("personalization", {}).get("match_score", 0),
            reverse=True
        )
        
        return {
            "success": True,
            "count": len(personalized_events),
            "events": personalized_events
        }
        
    except Exception as e:
        logger.error(f"[API] Batch personalization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
