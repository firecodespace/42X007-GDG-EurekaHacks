import asyncio
from typing import List
from app.queue.queue_manager import queue_manager, QueueStatus
from app.queue.rate_limiter import rate_limiter
from app.orchestration.pipeline import extraction_pipeline
from app.persistence.firestore_repo import firestore_repo
from app.shared.logger import logger


class QueueProcessor:
    """Process extraction queue with rate limiting"""
    
    async def process_queue(self, max_concurrent: int = 3):
        """
        Process pending items in queue
        
        Args:
            max_concurrent: Max parallel extractions
        """
        logger.info("[Processor] Starting queue processing...")
        
        # Get queue stats
        stats = await queue_manager.get_queue_stats()
        logger.info(f"[Processor] Queue stats: {stats}")
        
        # Get next batch
        batch = await queue_manager.get_next_batch(batch_size=max_concurrent)
        
        if not batch:
            logger.info("[Processor] No items in queue")
            return
        
        # Process items concurrently with rate limiting
        tasks = []
        for item in batch:
            if rate_limiter.can_proceed():
                tasks.append(self._process_item(item))
                rate_limiter.increment()
            else:
                wait_time = rate_limiter.get_wait_time()
                logger.warning(f"[Processor] Rate limit reached. Wait {wait_time}s")
                break
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _process_item(self, item: dict):
        """Process single queue item"""
        queue_id = item["id"]
        url = item["url"]
        platform = item["platform"]
        
        try:
            logger.info(f"[Processor] Processing: {url}")
            
            # Update status to processing
            await queue_manager.update_status(queue_id, QueueStatus.PROCESSING)
            
            # Extract event
            event = await extraction_pipeline.extract_event(url)
            
            if event:
                # Save to Firestore
                event_id = await firestore_repo.create_event(event)
                
                # Update queue status
                await queue_manager.update_status(queue_id, QueueStatus.COMPLETED)
                
                # Log success
                await queue_manager.log_extraction(
                    url, platform, "success", event_id=event_id
                )
                
                logger.info(f"[Processor] ✅ Success: {url} -> {event_id}")
            else:
                raise Exception("Extraction returned None")
                
        except Exception as e:
            logger.error(f"[Processor] ❌ Failed: {url} - {e}")
            
            # Update queue status
            await queue_manager.update_status(
                queue_id, QueueStatus.FAILED, error=str(e)
            )
            
            # Log failure
            await queue_manager.log_extraction(
                url, platform, "failed", error=str(e)
            )


queue_processor = QueueProcessor()
