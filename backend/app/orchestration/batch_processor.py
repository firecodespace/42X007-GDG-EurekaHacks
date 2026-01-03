from typing import List, Dict, Any, Optional
from datetime import datetime
from app.orchestration.pipeline import extraction_pipeline
from app.domain.event import Event
from app.discovery.unstop_indexer import UnstopIndexer
from app.shared.logger import logger


class BatchProcessor:
    """Batch processing for platform discovery and extraction"""
    
    def __init__(self):
        self.indexers = {
            "unstop": UnstopIndexer(),
        }
    
    async def process_platform(
        self,
        platform: str,
        max_pages: Optional[int] = 3,
        max_concurrent: int = 5
    ) -> Dict[str, Any]:
        """
        Complete pipeline: discover URLs -> extract events
        
        Args:
            platform: Platform name (unstop, devpost, etc.)
            max_pages: Max pages to discover
            max_concurrent: Max concurrent extractions
            
        Returns:
            Dict with processing results and statistics
        """
        start_time = datetime.utcnow()
        
        logger.info(f"[BatchProcessor] Starting {platform} processing")
        
        indexer = self.indexers.get(platform.lower())
        if not indexer:
            logger.error(f"[BatchProcessor] Unknown platform: {platform}")
            return {"error": f"Platform '{platform}' not supported"}
        
        discovery_result = await indexer.discover_with_metadata(
            max_pages=max_pages
        )
        
        urls = discovery_result.get("urls", [])
        
        if not urls:
            logger.warning(f"[BatchProcessor] No URLs discovered from {platform}")
            return {
                "platform": platform,
                "urls_discovered": 0,
                "events_extracted": 0,
                "events": []
            }
        
        logger.info(
            f"[BatchProcessor] Discovered {len(urls)} URLs, starting extraction..."
        )
        
        events = await extraction_pipeline.extract_batch(
            urls,
            max_concurrent=max_concurrent
        )
        
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds()
        
        result = {
            "platform": platform,
            "urls_discovered": len(urls),
            "events_extracted": len(events),
            "success_rate": len(events) / len(urls) if urls else 0,
            "duration_seconds": duration,
            "events": [
                {
                    "id": event.id,
                    "title": event.title,
                    "url": event.source_url,
                    "confidence": event.confidence_score
                }
                for event in events
            ],
            "timestamp": end_time.isoformat()
        }
        
        logger.info(
            f"[BatchProcessor] {platform} processing complete: "
            f"{len(events)}/{len(urls)} extracted in {duration:.2f}s"
        )
        
        return result


batch_processor = BatchProcessor()
