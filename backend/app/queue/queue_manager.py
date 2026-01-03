from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from google.cloud.firestore import Client
from app.config.firebase_config import get_firestore_client
from app.shared.logger import logger
from enum import Enum


class QueueStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"


class QueueManager:
    """Manage extraction queue in Firestore"""
    
    QUEUE_COLLECTION = "extraction_queue"
    LOGS_COLLECTION = "extraction_logs"
    
    def __init__(self):
        self._db: Optional[Client] = None
    
    @property
    def db(self) -> Client:
        """Lazy load Firestore client"""
        if self._db is None:
            self._db = get_firestore_client()
        return self._db
    
    async def add_to_queue(
        self, 
        url: str, 
        platform: str, 
        priority: int = 0
    ) -> str:
        """
        Add URL to extraction queue
        
        Args:
            url: URL to extract
            platform: Platform name
            priority: Priority (higher = processed first)
            
        Returns:
            Queue item ID
        """
        try:
            # Check if URL already in queue or processed
            existing = self.db.collection(self.QUEUE_COLLECTION)\
                .where("url", "==", url)\
                .limit(1)\
                .stream()
            
            for doc in existing:
                logger.info(f"[Queue] URL already in queue: {url}")
                return doc.id
            
            # Check if already extracted
            from app.persistence.firestore_repo import firestore_repo
            if await firestore_repo.event_exists(url):
                logger.info(f"[Queue] Event already extracted: {url}")
                return None
            
            # Add to queue
            queue_item = {
                "url": url,
                "platform": platform,
                "status": QueueStatus.PENDING,
                "priority": priority,
                "attempts": 0,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "next_retry_at": datetime.utcnow()
            }
            
            doc_ref = self.db.collection(self.QUEUE_COLLECTION).document()
            doc_ref.set(queue_item)
            
            logger.info(f"[Queue] Added to queue: {url} (ID: {doc_ref.id})")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"[Queue] Failed to add URL: {e}")
            raise
    
    async def get_next_batch(self, batch_size: int = 5) -> List[Dict[str, Any]]:
        """
        Get next batch of URLs to process
        
        Args:
            batch_size: Number of URLs to fetch
            
        Returns:
            List of queue items
        """
        try:
            # Get pending items that are ready for processing
            query = self.db.collection(self.QUEUE_COLLECTION)\
                .where("status", "==", QueueStatus.PENDING)\
                .where("next_retry_at", "<=", datetime.utcnow())\
                .order_by("priority", direction="DESCENDING")\
                .order_by("created_at")\
                .limit(batch_size)
            
            items = []
            for doc in query.stream():
                item = doc.to_dict()
                item["id"] = doc.id
                items.append(item)
            
            logger.info(f"[Queue] Fetched {len(items)} items for processing")
            return items
            
        except Exception as e:
            logger.error(f"[Queue] Failed to fetch batch: {e}")
            return []
    
    async def update_status(
        self, 
        queue_id: str, 
        status: QueueStatus, 
        error: Optional[str] = None
    ):
        """Update queue item status"""
        try:
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow()
            }
            
            if status == QueueStatus.PROCESSING:
                update_data["processing_started_at"] = datetime.utcnow()
            
            if status == QueueStatus.COMPLETED:
                update_data["completed_at"] = datetime.utcnow()
            
            if status == QueueStatus.FAILED:
                update_data["error"] = error
                update_data["attempts"] = self.db.collection(self.QUEUE_COLLECTION)\
                    .document(queue_id).get().to_dict().get("attempts", 0) + 1
                # Retry after 1 hour
                update_data["next_retry_at"] = datetime.utcnow() + timedelta(hours=1)
            
            self.db.collection(self.QUEUE_COLLECTION)\
                .document(queue_id).update(update_data)
            
            logger.info(f"[Queue] Updated {queue_id} to {status}")
            
        except Exception as e:
            logger.error(f"[Queue] Failed to update status: {e}")
    
    async def log_extraction(
        self, 
        url: str, 
        platform: str, 
        status: str, 
        event_id: Optional[str] = None,
        error: Optional[str] = None
    ):
        """Log extraction attempt"""
        try:
            log_entry = {
                "url": url,
                "platform": platform,
                "status": status,
                "event_id": event_id,
                "error": error,
                "timestamp": datetime.utcnow()
            }
            
            self.db.collection(self.LOGS_COLLECTION).add(log_entry)
            
        except Exception as e:
            logger.error(f"[Queue] Failed to log extraction: {e}")
    
    async def get_queue_stats(self) -> Dict[str, int]:
        """Get queue statistics"""
        try:
            stats = {
                "pending": 0,
                "processing": 0,
                "completed": 0,
                "failed": 0
            }
            
            for status in QueueStatus:
                count = len(list(
                    self.db.collection(self.QUEUE_COLLECTION)
                    .where("status", "==", status.value)
                    .stream()
                ))
                stats[status.value] = count
            
            return stats
            
        except Exception as e:
            logger.error(f"[Queue] Failed to get stats: {e}")
            return {}


queue_manager = QueueManager()
