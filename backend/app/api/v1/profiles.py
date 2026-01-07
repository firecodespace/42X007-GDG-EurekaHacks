from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models.user_profile import UserProfile
from app.persistence.profile_repo import profile_repo
from app.services.recommendation_cache import recommendation_cache
from app.shared.logger import logger

router = APIRouter()


@router.post("/", status_code=201)
async def create_profile(profile: UserProfile) -> Dict[str, Any]:
    """
    Create a new user profile
    
    **Example:**
    ```json
    {
      "user_id": "user123",
      "skills": ["Python", "React", "Machine Learning"],
      "interests": ["AI/ML", "Web Development"],
      "experience_level": "intermediate"
    }
    ```
    """
    try:
        # Check if profile already exists
        existing = await profile_repo.get_profile(profile.user_id)
        if existing:
            raise HTTPException(status_code=400, detail="Profile already exists")
        
        user_id = await profile_repo.create_profile(profile)
        
        return {
            "success": True,
            "user_id": user_id,
            "message": "Profile created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] Create profile error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}")
async def get_profile(user_id: str) -> UserProfile:
    """Get user profile by ID"""
    try:
        profile = await profile_repo.get_profile(user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return profile
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] Get profile error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}")
async def update_profile(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update user profile
    
    **Example:**
    ```json
    {
      "skills": ["Python", "React", "Docker", "Kubernetes"],
      "interests": ["AI/ML", "DevOps", "Cloud Computing"]
    }
    ```
    """
    try:
        # Check if profile exists
        profile = await profile_repo.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Update profile
        success = await profile_repo.update_profile(user_id, updates)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update profile")
        
        # Invalidate cache when profile changes
        invalidated = await recommendation_cache.invalidate_user_cache(user_id)
        logger.info(f"[API] Invalidated {invalidated} cache entries for {user_id}")
        
        return {
            "success": True,
            "user_id": user_id,
            "message": "Profile updated successfully",
            "cache_invalidated": invalidated
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[API] Update profile error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}")
async def delete_profile(user_id: str) -> Dict[str, Any]:
    """Delete user profile"""
    try:
        success = await profile_repo.delete_profile(user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {
            "success": True,
            "message": "Profile deleted successfully"
        }
        
    except Exception as e:
        logger.error(f"[API] Delete profile error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_profiles(limit: int = 50) -> List[UserProfile]:
    """List all user profiles"""
    try:
        profiles = await profile_repo.list_profiles(limit=limit)
        return profiles
        
    except Exception as e:
        logger.error(f"[API] List profiles error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/events")
async def add_event_to_history(
    user_id: str,
    event: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Add event to user's attended history
    
    **Example:**
    ```json
    {
      "event_id": "79d48242750f7ffb",
      "name": "ProdWars - IIT Delhi",
      "date": "2026-01-10"
    }
    ```
    """
    try:
        success = await profile_repo.add_event_to_history(user_id, event)
        
        if not success:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        return {
            "success": True,
            "message": "Event added to history"
        }
        
    except Exception as e:
        logger.error(f"[API] Add event to history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
