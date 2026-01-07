from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from app.config.firebase_config import get_firestore_client
from app.shared.logger import logger


class RecommendationCache:
    """Cache personalized recommendations in Firestore"""
    
    COLLECTION = "recommendation_cache"
    TTL_HOURS = 24
    
    def __init__(self):
        self._db = None
    
    @property
    def db(self):
        if self._db is None:
            self._db = get_firestore_client()
        return self._db
    
    def _cache_key(self, user_id: str, event_id: str) -> str:
        return f"{user_id}_{event_id}"
    
    async def get_cached(self, user_id: str, event_id: str) -> Optional[Dict[str, Any]]:
        try:
            cache_key = self._cache_key(user_id, event_id)
            doc = self.db.collection(self.COLLECTION).document(cache_key).get()
            
            if not doc.exists:
                return None
            
            data = doc.to_dict()
            cached_at = data.get("cached_at")
            
            if cached_at:
                age = datetime.utcnow() - cached_at
                if age > timedelta(hours=self.TTL_HOURS):
                    return None
            
            logger.info(f"[Cache] HIT: {cache_key}")
            return data.get("personalization")
            
        except Exception as e:
            logger.error(f"[Cache] Get error: {e}")
            return None
    
    async def set_cached(
        self, 
        user_id: str, 
        event_id: str, 
        personalization: Dict[str, Any]
    ) -> bool:
        try:
            cache_key = self._cache_key(user_id, event_id)
            
            data = {
                "user_id": user_id,
                "event_id": event_id,
                "personalization": personalization,
                "cached_at": datetime.utcnow()
            }
            
            self.db.collection(self.COLLECTION).document(cache_key).set(data)
            logger.info(f"[Cache] SET: {cache_key}")
            return True
            
        except Exception as e:
            logger.error(f"[Cache] Set error: {e}")
            return False
    
    async def invalidate_user_cache(self, user_id: str) -> int:
        try:
            docs = self.db.collection(self.COLLECTION)\
                .where("user_id", "==", user_id)\
                .stream()
            
            count = 0
            for doc in docs:
                doc.reference.delete()
                count += 1
            
            logger.info(f"[Cache] Invalidated {count} entries for {user_id}")
            return count
            
        except Exception as e:
            logger.error(f"[Cache] Invalidate error: {e}")
            return 0


recommendation_cache = RecommendationCache()
