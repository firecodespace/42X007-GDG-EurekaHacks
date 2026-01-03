from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.domain.extraction_result import ExtractionResult, ExtractionStatus, ExtractionEngine
from app.shared.logger import logger
import time


class BaseEngine(ABC):
    """Abstract base class for all extraction engines"""
    
    def __init__(self, engine_type: ExtractionEngine):
        self.engine_type = engine_type
    
    @abstractmethod
    async def extract(self, url: str, platform: str) -> Dict[str, Any]:
        """
        Extract data from URL and return raw dictionary
        
        Args:
            url: URL to extract from
            platform: Platform name (unstop, devpost, etc.)
            
        Returns:
            Dict containing extracted raw data
        """
        pass
    
    @abstractmethod
    def supports_url(self, url: str) -> bool:
        """
        Check if this engine can handle the given URL
        
        Args:
            url: URL to check
            
        Returns:
            True if engine supports this URL
        """
        pass
    
    async def extract_with_metadata(self, url: str, platform: str) -> ExtractionResult:
        """
        Extract data and wrap in ExtractionResult with metadata
        
        Args:
            url: URL to extract from
            platform: Platform name
            
        Returns:
            ExtractionResult with status, timing, and data
        """
        start_time = time.time()
        
        try:
            logger.info(f"[{self.engine_type.value}] Starting extraction: {url}")
            
            raw_data = await self.extract(url, platform)
            
            extraction_time = time.time() - start_time
            
            logger.info(
                f"[{self.engine_type.value}] Extraction successful: {url} "
                f"(took {extraction_time:.2f}s)"
            )
            
            return ExtractionResult(
                url=url,
                platform=platform,
                status=ExtractionStatus.SUCCESS,
                engine_used=self.engine_type,
                raw_data=raw_data,
                extraction_time=extraction_time,
                metadata={
                    "fields_extracted": len(raw_data.keys()) if raw_data else 0
                }
            )
            
        except Exception as e:
            extraction_time = time.time() - start_time
            
            logger.error(
                f"[{self.engine_type.value}] Extraction failed: {url} - {str(e)}"
            )
            
            return ExtractionResult(
                url=url,
                platform=platform,
                status=ExtractionStatus.FAILED,
                engine_used=self.engine_type,
                error_message=str(e),
                extraction_time=extraction_time
            )
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify engine is operational
        
        Returns:
            True if engine is healthy
        """
        pass
