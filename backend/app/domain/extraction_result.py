from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class ExtractionStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    PENDING = "pending"


class ExtractionEngine(str, Enum):
    TRADITIONAL_SCRAPER = "traditional_scraper"
    BROWSER_AUTOMATION = "browser_automation"
    GEMINI_GROUNDING = "gemini_grounding"
    CUSTOM_AI_SCRAPER = "custom_ai_scraper"
    CRAWL4AI = "crawl4ai"


class ExtractionResult(BaseModel):
    url: str
    platform: str
    
    status: ExtractionStatus
    engine_used: ExtractionEngine
    
    raw_data: Optional[Dict[str, Any]] = None
    normalized_data: Optional[Dict[str, Any]] = None
    
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    error_message: Optional[str] = None
    
    extraction_time: float = 0.0
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        use_enum_values = True


class ExtractionMetrics(BaseModel):
    """Metrics for monitoring extraction performance"""
    total_attempts: int = 0
    successful_extractions: int = 0
    failed_extractions: int = 0
    
    average_extraction_time: float = 0.0
    
    engine_success_rates: Dict[str, float] = Field(default_factory=dict)
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)
