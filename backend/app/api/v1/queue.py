from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from app.queue.queue_manager import queue_manager, QueueStatus
from app.queue.processor import queue_processor
from app.queue.scheduler import automated_scheduler
from app.shared.logger import logger


router = APIRouter()


class BatchURLRequest(BaseModel):
    """Request model for batch URL addition"""
    urls: List[str]
    platform: str = "Unknown"


@router.post("/add")
async def add_to_queue(url: str, platform: str = "Unknown", priority: int = 0):
    """
    Manually add URL to extraction queue
    
    Args:
        url: URL to extract
        platform: Platform name
        priority: Priority (0-10, higher = processed first)
    """
    try:
        queue_id = await queue_manager.add_to_queue(url, platform, priority)
        
        if not queue_id:
            return {
                "success": False,
                "message": "URL already exists or was already extracted"
            }
        
        return {
            "success": True,
            "queue_id": queue_id,
            "message": "Added to extraction queue"
        }
        
    except Exception as e:
        logger.error(f"[API] Failed to add to queue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/add-batch")
async def add_batch_to_queue(request: BatchURLRequest):
    """
    Add multiple URLs to queue
    
    Args:
        request: Batch URL request with urls and platform
    """
    try:
        added = []
        skipped = []
        
        for url in request.urls:
            queue_id = await queue_manager.add_to_queue(url, request.platform)
            if queue_id:
                added.append(url)
            else:
                skipped.append(url)
        
        return {
            "success": True,
            "added": len(added),
            "skipped": len(skipped),
            "total": len(request.urls),
            "added_urls": added,
            "skipped_urls": skipped
        }
        
    except Exception as e:
        logger.error(f"[API] Failed to add batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_queue_stats():
    """Get queue statistics"""
    try:
        stats = await queue_manager.get_queue_stats()
        return stats
    except Exception as e:
        logger.error(f"[API] Failed to get stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process")
async def process_queue_manually(max_concurrent: int = Query(3, ge=1, le=10)):
    """
    Manually trigger queue processing
    
    Args:
        max_concurrent: Max concurrent extractions
    """
    try:
        logger.info(f"[API] Manual queue processing triggered")
        await queue_processor.process_queue(max_concurrent=max_concurrent)
        
        return {
            "success": True,
            "message": "Queue processing completed"
        }
        
    except Exception as e:
        logger.error(f"[API] Queue processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scheduler/status")
async def get_scheduler_status():
    """Get scheduler status"""
    try:
        return {
            "running": automated_scheduler.is_running,
            "jobs": [
                {
                    "id": job.id,
                    "name": job.name,
                    "next_run": job.next_run_time.isoformat() if job.next_run_time else None
                }
                for job in automated_scheduler.scheduler.get_jobs()
            ] if automated_scheduler.is_running else []
        }
    except Exception as e:
        logger.error(f"[API] Failed to get scheduler status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scheduler/start")
async def start_scheduler():
    """Start the scheduler"""
    try:
        automated_scheduler.start()
        return {"success": True, "message": "Scheduler started"}
    except Exception as e:
        logger.error(f"[API] Failed to start scheduler: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scheduler/stop")
async def stop_scheduler():
    """Stop the scheduler"""
    try:
        automated_scheduler.stop()
        return {"success": True, "message": "Scheduler stopped"}
    except Exception as e:
        logger.error(f"[API] Failed to stop scheduler: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scheduler/trigger/{job_id}")
async def trigger_job(job_id: str):
    """
    Manually trigger a scheduled job
    
    Args:
        job_id: Job ID (process_queue, discover_unstop, cleanup, stats_report)
    """
    try:
        automated_scheduler.run_job_now(job_id)
        return {
            "success": True,
            "message": f"Job {job_id} triggered"
        }
    except Exception as e:
        logger.error(f"[API] Failed to trigger job: {e}")
        raise HTTPException(status_code=500, detail=str(e))
