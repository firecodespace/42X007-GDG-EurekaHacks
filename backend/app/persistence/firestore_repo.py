from typing import Optional, List, Dict, Any
from datetime import datetime
from google.cloud.firestore import Client
from app.config.firebase_config import get_firestore_client
from app.domain.event import Event, EventCreate, EventUpdate
from app.shared.logger import logger
from app.shared.exceptions import PersistenceError
import hashlib


class FirestoreRepository:
    """Repository for Event persistence in Firestore"""
    
    COLLECTION_NAME = "events"
    
    def __init__(self):
        self._db: Optional[Client] = None
    
    @property
    def db(self) -> Client:
        """Lazy load Firestore client"""
        if self._db is None:
            self._db = get_firestore_client()
        return self._db
    
    def _generate_event_id(self, url: str) -> str:
        """Generate deterministic event ID from URL"""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    async def create_event(self, event: Event) -> str:
        """
        Create new event in Firestore
        
        Args:
            event: Event object to create
            
        Returns:
            Created event ID
        """
        try:
            if not event.id:
                event.id = self._generate_event_id(event.source_url)
            
            event_dict = event.dict(exclude_none=False)
            event_dict["created_at"] = datetime.utcnow()
            event_dict["updated_at"] = datetime.utcnow()
            
            self.db.collection(self.COLLECTION_NAME).document(event.id).set(
                event_dict
            )
            
            logger.info(f"[Firestore] Created event: {event.id} - {event.title}")
            
            return event.id
            
        except Exception as e:
            logger.error(f"[Firestore] Failed to create event: {e}")
            raise PersistenceError(f"Failed to create event: {e}")
    
    async def get_event(self, event_id: str) -> Optional[Event]:
        """Get event by ID"""
        try:
            doc = self.db.collection(self.COLLECTION_NAME).document(event_id).get()
            
            if not doc.exists:
                return None
            
            event_data = doc.to_dict()
            return Event(**event_data)
            
        except Exception as e:
            logger.error(f"[Firestore] Failed to get event {event_id}: {e}")
            return None
    
    async def update_event(self, event_id: str, update: EventUpdate) -> bool:
        """Update existing event"""
        try:
            update_dict = update.dict(exclude_none=True)
            update_dict["updated_at"] = datetime.utcnow()
            
            self.db.collection(self.COLLECTION_NAME).document(event_id).update(
                update_dict
            )
            
            logger.info(f"[Firestore] Updated event: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"[Firestore] Failed to update event {event_id}: {e}")
            return False
    
    async def delete_event(self, event_id: str) -> bool:
        """Delete event"""
        try:
            self.db.collection(self.COLLECTION_NAME).document(event_id).delete()
            logger.info(f"[Firestore] Deleted event: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"[Firestore] Failed to delete event {event_id}: {e}")
            return False
    
    async def list_events(
        self,
        limit: int = 50,
        offset: int = 0,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Event]:
        """List events with pagination and filters"""
        try:
            query = self.db.collection(self.COLLECTION_NAME)
            
            if filters:
                if "platform" in filters:
                    query = query.where("source_platform", "==", filters["platform"])
                
                if "mode" in filters:
                    query = query.where("mode", "==", filters["mode"])
            
            query = query.order_by("created_at", direction="DESCENDING")
            query = query.limit(limit).offset(offset)
            
            docs = query.stream()
            
            events = []
            for doc in docs:
                try:
                    event = Event(**doc.to_dict())
                    events.append(event)
                except Exception as e:
                    logger.warning(f"[Firestore] Failed to parse event {doc.id}: {e}")
                    continue
            
            logger.info(f"[Firestore] Listed {len(events)} events")
            return events
            
        except Exception as e:
            logger.error(f"[Firestore] Failed to list events: {e}")
            return []
    
    async def event_exists(self, url: str) -> bool:
        """Check if event with URL already exists"""
        event_id = self._generate_event_id(url)
        doc = self.db.collection(self.COLLECTION_NAME).document(event_id).get()
        return doc.exists
    
    async def get_events_by_platform(self, platform: str, limit: int = 50) -> List[Event]:
        """Get events from specific platform"""
        return await self.list_events(
            limit=limit,
            filters={"platform": platform}
        )


firestore_repo = FirestoreRepository()
