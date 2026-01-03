from fastapi import APIRouter
from app.api.v1 import health, events, discovery, queue

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(discovery.router, prefix="/discovery", tags=["discovery"])
api_router.include_router(queue.router, prefix="/queue", tags=["queue"])
