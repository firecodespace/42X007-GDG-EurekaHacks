from typing import Optional, List
from datetime import datetime
from google.cloud.firestore import Client
from app.config.firebase_config import get_firestore_client
from app.models.user_profile import UserProfile
from app.shared.logger import logger


class ProfileRepository:
    """Repository for User Profile persistence in Firestore"""
    
    COLLECTION_NAME = "user_profiles"
    
    def __init__(self):
        self._db: Optional[Client] = None
    
    @property
    def db(self) -> Client:
        """Lazy load Firestore client"""
        if self._db is None:
            self._db = get_firestore_client()
        return self._db
    
    async def create_profile(self, profile: UserProfile) -> str:
        """Create new user profile"""
        try:
            profile_dict = profile.dict()
            profile_dict["created_at"] = datetime.utcnow()
            profile_dict["updated_at"] = datetime.utcnow()
            
            self.db.collection(self.COLLECTION_NAME).document(profile.user_id).set(
                profile_dict
            )
            
            logger.info(f"[ProfileRepo] Created profile: {profile.user_id}")
            return profile.user_id
            
        except Exception as e:
            logger.error(f"[ProfileRepo] Failed to create profile: {e}")
            raise
    
    async def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID"""
        try:
            doc = self.db.collection(self.COLLECTION_NAME).document(user_id).get()
            
            if not doc.exists:
                return None
            
            profile_data = doc.to_dict()
            return UserProfile(**profile_data)
            
        except Exception as e:
            logger.error(f"[ProfileRepo] Failed to get profile {user_id}: {e}")
            return None
    
    async def update_profile(self, user_id: str, updates: dict) -> bool:
        """Update user profile"""
        try:
            updates["updated_at"] = datetime.utcnow()
            
            self.db.collection(self.COLLECTION_NAME).document(user_id).update(updates)
            
            logger.info(f"[ProfileRepo] Updated profile: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"[ProfileRepo] Failed to update profile {user_id}: {e}")
            return False
    
    async def delete_profile(self, user_id: str) -> bool:
        """Delete user profile"""
        try:
            self.db.collection(self.COLLECTION_NAME).document(user_id).delete()
            logger.info(f"[ProfileRepo] Deleted profile: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"[ProfileRepo] Failed to delete profile {user_id}: {e}")
            return False
    
    async def list_profiles(self, limit: int = 50) -> List[UserProfile]:
        """List all profiles"""
        try:
            docs = self.db.collection(self.COLLECTION_NAME)\
                .order_by("created_at", direction="DESCENDING")\
                .limit(limit)\
                .stream()
            
            profiles = []
            for doc in docs:
                try:
                    profile = UserProfile(**doc.to_dict())
                    profiles.append(profile)
                except Exception as e:
                    logger.warning(f"[ProfileRepo] Failed to parse profile {doc.id}: {e}")
                    continue
            
            return profiles
            
        except Exception as e:
            logger.error(f"[ProfileRepo] Failed to list profiles: {e}")
            return []
    
    async def add_event_to_history(self, user_id: str, event: dict) -> bool:
        """Add event to user's attended events"""
        try:
            profile = await self.get_profile(user_id)
            if not profile:
                return False
            
            profile.events_attended.append(event)
            
            await self.update_profile(user_id, {
                "events_attended": [e for e in profile.events_attended]
            })
            
            logger.info(f"[ProfileRepo] Added event to {user_id} history")
            return True
            
        except Exception as e:
            logger.error(f"[ProfileRepo] Failed to add event to history: {e}")
            return False


profile_repo = ProfileRepository()
