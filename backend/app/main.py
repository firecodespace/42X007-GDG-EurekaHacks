from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings, initialize_firebase, initialize_gemini, close_firebase
from app.api import api_router
from app.shared.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting HackFlix Backend...")
    
    try:
        initialize_firebase()
        initialize_gemini()
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    yield
    
    logger.info("Shutting down HackFlix Backend...")
    close_firebase()


app = FastAPI(
    title="HackFlix API",
    description="AI-driven event discovery platform for hackathons and competitions",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "HackFlix API",
        "version": "1.0.0",
        "docs": "/docs"
    }
