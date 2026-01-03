from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.orchestration.batch_processor import batch_processor
from app.persistence.firestore_repo import firestore_repo
from app.shared.logger import logger

router = APIRouter()


@router.post("/discover/{platform}")
async def discover_platform(
    platform: str,
    max_pages: int = Query(3, ge=1, le=10),
    max_concurrent: int = Query(5, ge=1, le=10),
    save_to_db: bool = Query(True)
):
    """
    Discover and extract events from platform
    
    Args:
        platform: Platform name (unstop, devpost, etc.)
        max_pages: Maximum pages to crawl
        max_concurrent: Maximum concurrent extractions
        save_to_db: Whether to save events to database
    """
    try:
        logger.info(f"[API] Discovery request for platform: {platform}")
        
        result = await batch_processor.process_platform(
            platform=platform,
            max_pages=max_pages,
            max_concurrent=max_concurrent
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        if save_to_db and result.get("events"):
            from app.orchestration.pipeline import extraction_pipeline
            
            saved_count = 0
            for event_summary in result["events"]:
                try:
                    event = await extraction_pipeline.extract_event(
                        event_summary["url"]
                    )
                    if event:
                        await firestore_repo.create_event(event)
                        saved_count += 1
                except Exception as e:
                    logger.warning(f"[API] Failed to save event: {e}")
                    continue
            
            result["saved_to_db"] = saved_count
        
        return result
        
    except Exception as e:
        logger.error(f"[API] Discovery failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platforms")
async def list_platforms():
    """List supported platforms"""
    return {
        "platforms": [
            {
                "name": "Unstop",
                "key": "unstop",
                "status": "active",
                "types": ["hackathons", "competitions"]
            },
            {
                "name": "Devpost",
                "key": "devpost",
                "status": "planned",
                "types": ["hackathons"]
            },
            {
                "name": "Devfolio",
                "key": "devfolio",
                "status": "planned",
                "types": ["hackathons"]
            },
            {
                "name": "Hack2Skill",
                "key": "hack2skill",
                "status": "planned",
                "types": ["hackathons", "competitions"]
            },
            {
                "name": "Devnovate",
                "key": "devnovate",
                "status": "planned",
                "types": ["competitions"]
            }
        ]
    }
