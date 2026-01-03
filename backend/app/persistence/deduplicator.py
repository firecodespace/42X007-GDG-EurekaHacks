from typing import Optional
from app.domain.event import Event
from app.persistence.firestore_repo import firestore_repo
from app.shared.logger import logger


class EventDeduplicator:
    """Handle event deduplication logic"""
    
    async def is_duplicate(self, event: Event) -> bool:
        """
        Check if event is duplicate based on URL
        
        Args:
            event: Event to check
            
        Returns:
            True if duplicate exists
        """
        exists = await firestore_repo.event_exists(event.source_url)
        
        if exists:
            logger.info(f"[Deduplicator] Duplicate found: {event.source_url}")
        
        return exists
    
    async def get_existing_event(self, url: str) -> Optional[Event]:
        """Get existing event by URL"""
        import hashlib
        event_id = hashlib.sha256(url.encode()).hexdigest()[:16]
        return await firestore_repo.get_event(event_id)
    
    async def should_update(self, new_event: Event, existing_event: Event) -> bool:
        """
        Determine if existing event should be updated with new data
        
        Args:
            new_event: Newly extracted event
            existing_event: Existing event in database
            
        Returns:
            True if should update
        """
        if new_event.confidence_score > existing_event.confidence_score:
            logger.info(
                f"[Deduplicator] New extraction has higher confidence: "
                f"{new_event.confidence_score} > {existing_event.confidence_score}"
            )
            return True
        
        if new_event.updated_at > existing_event.updated_at:
            logger.info("[Deduplicator] New extraction is more recent")
            return True
        
        return False


event_deduplicator = EventDeduplicator()
