from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.api.v1 import api_router
from app.shared.logger import logger
from app.config.firebase_config import initialize_firebase
from app.config.gemini_config import initialize_gemini
from app.queue.scheduler import automated_scheduler

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting HackFlix Backend...")
    
    # Initialize services
    initialize_firebase()
    initialize_gemini()
    
    # Start automated scheduler if enabled
    scheduler_enabled = os.getenv("SCHEDULER_ENABLED", "false").lower() == "true"
    if scheduler_enabled:
        automated_scheduler.start()
        logger.info("✅ Automated scheduler started")
    else:
        logger.info("⚠️  Automated scheduler is DISABLED (set SCHEDULER_ENABLED=true to enable)")
    
    logger.info("All services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down HackFlix Backend...")
    if scheduler_enabled:
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
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "HackFlix API",
        "version": "1.0.0",
        "status": "running"
    }
