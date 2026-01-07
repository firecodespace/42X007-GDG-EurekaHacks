from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.shared.logger import logger
from app.config.firebase_config import initialize_firebase
from app.config.gemini_config import initialize_gemini
from app.queue.scheduler import automated_scheduler

# Import individual routers
from app.api.v1 import events, queue, personalization, profiles, recommendations

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting HackFlix Backend...")
    
    # Initialize services
    initialize_firebase()
    initialize_gemini()
    
    # Start automated scheduler
    automated_scheduler.start()
    logger.info("✅ Automated scheduler started")
    
    logger.info("All services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down HackFlix Backend...")
    automated_scheduler.stop()
    logger.info("Scheduler stopped")

app = FastAPI(
    title="HackFlix API",
    description="AI-powered hackathon discovery and extraction platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(
    events.router,
    prefix="/api/v1/events",
    tags=["Events"]
)

app.include_router(
    queue.router,
    prefix="/api/v1/queue",
    tags=["Queue"]
)

app.include_router(
    personalization.router,
    prefix="/api/v1/personalization",
    tags=["Personalization"]
)

app.include_router(
    profiles.router,
    prefix="/api/v1/profiles",
    tags=["Profiles"]
)

app.include_router(
    recommendations.router,
    prefix="/api/v1/recommendations",
    tags=["Recommendations"]
)

@app.get("/")
async def root():
    return {
        "message": "HackFlix API",
        "version": "1.0.0",
        "status": "running"
    }
