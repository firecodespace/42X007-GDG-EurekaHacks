from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.domain.event import Event, EventResponse
from app.persistence.firestore_repo import firestore_repo
from app.orchestration.pipeline import extraction_pipeline
from app.shared.logger import logger

router = APIRouter()


@router.get("/", response_model=List[EventResponse])
async def list_events(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    platform: Optional[str] = None,
    mode: Optional[str] = None
):
    """List events with pagination and filters"""
    filters = {}
    if platform:
        filters["platform"] = platform
    if mode:
        filters["mode"] = mode
    
    events = await firestore_repo.list_events(
        limit=limit,
        offset=offset,
        filters=filters
    )
    
    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    """Get specific event by ID"""
    event = await firestore_repo.get_event(event_id)
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event


@router.post("/extract")
async def extract_event(url: str):
    """Extract event from URL"""
    try:
        logger.info(f"[API] Extract request for: {url}")
        
        event = await extraction_pipeline.extract_event(url)
        
        if not event:
            raise HTTPException(
                status_code=422,
                detail="Failed to extract event from URL"
            )
        
        event_id = await firestore_repo.create_event(event)
        
        return {
            "success": True,
            "event_id": event_id,
            "title": event.title,
            "confidence_score": event.confidence_score
        }
        
    except Exception as e:
        logger.error(f"[API] Extract failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{event_id}")
async def delete_event(event_id: str):
    """Delete event"""
    success = await firestore_repo.delete_event(event_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return {"success": True, "message": "Event deleted"}
