from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.config.settings import settings
from app.config.firebase_config import get_firestore_client
from app.shared.logger import logger

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    environment: str
    version: str = "1.0.0"


class DetailedHealthResponse(HealthResponse):
    services: dict


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        environment=settings.environment
    )


@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """Detailed health check with service status"""
    services = {}
    
    try:
        db = get_firestore_client()
        db.collection("_health_check").document("test").set({"ping": "pong"})
        services["firestore"] = "healthy"
    except Exception as e:
        logger.error(f"Firestore health check failed: {e}")
        services["firestore"] = "unhealthy"
    
    try:
        from app.config.gemini_config import get_gemini_model
        model = get_gemini_model()
        services["gemini"] = "healthy" if model else "unhealthy"
    except Exception as e:
        logger.error(f"Gemini health check failed: {e}")
        services["gemini"] = "unhealthy"
    
    overall_status = "healthy" if all(
        status == "healthy" for status in services.values()
    ) else "degraded"
    
    return DetailedHealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        environment=settings.environment,
        services=services
    )
