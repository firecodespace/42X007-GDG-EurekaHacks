from typing import List, Optional, Dict, Any
from app.domain.event import Event
from app.domain.extraction_result import ExtractionResult, ExtractionStatus
from app.extraction.engines import TraditionalScraper, CustomAIScraper, GeminiGrounding
from app.extraction.strategy_router import strategy_router
from app.normalization.gemini_normalizer import gemini_normalizer
from app.normalization.confidence_scorer import confidence_scorer
from app.discovery.classifier import url_classifier
from app.shared.logger import logger
from app.shared.exceptions import ExtractionError


class ExtractionPipeline:
    """Main orchestration pipeline for event extraction"""
    
    def __init__(self):
        self.engines = {
            "traditional_scraper": TraditionalScraper(),
            "custom_ai_scraper": CustomAIScraper(),
            "gemini_grounding": GeminiGrounding(),
        }
    
    async def extract_event(self, url: str) -> Optional[Event]:
        """
        Complete extraction pipeline for single URL
        
        Args:
            url: URL to extract event from
            
        Returns:
            Normalized Event object or None if extraction fails
        """
        logger.info(f"[Pipeline] Starting extraction for: {url}")
        
        platform_name, platform_type = url_classifier.classify(url)
        
        strategies = strategy_router.select_strategy(url)
        
        extraction_result = await self._extract_with_fallback(
            url, 
            platform_name, 
            strategies
        )
        
        if extraction_result.status != ExtractionStatus.SUCCESS:
            logger.error(f"[Pipeline] All extraction strategies failed for: {url}")
            return None
        
        event = await self._normalize_extraction(
            extraction_result, 
            url, 
            platform_name
        )
        
        if event:
            event.confidence_score = confidence_scorer.calculate_score(event)
            logger.info(
                f"[Pipeline] Successfully extracted: {event.title} "
                f"(confidence: {event.confidence_score})"
            )
        
        return event
    
    async def _extract_with_fallback(
        self,
        url: str,
        platform: str,
        strategies: List
    ) -> ExtractionResult:
        """Try extraction with multiple engines using fallback chain"""
        
        for strategy in strategies:
            engine_name = strategy.value
            engine = self.engines.get(engine_name)
            
            if not engine:
                logger.warning(f"[Pipeline] Engine not found: {engine_name}")
                continue
            
            try:
                logger.info(f"[Pipeline] Trying engine: {engine_name}")
                
                result = await engine.extract_with_metadata(url, platform)
                
                if result.status == ExtractionStatus.SUCCESS:
                    logger.info(f"[Pipeline] Success with: {engine_name}")
                    return result
                
                logger.warning(
                    f"[Pipeline] {engine_name} failed: {result.error_message}"
                )
                
            except Exception as e:
                logger.error(f"[Pipeline] {engine_name} crashed: {e}")
                continue
        
        return ExtractionResult(
            url=url,
            platform=platform,
            status=ExtractionStatus.FAILED,
            engine_used=strategies[0] if strategies else None,
            error_message="All extraction strategies failed"
        )
    
    async def _normalize_extraction(
        self,
        extraction_result: ExtractionResult,
        url: str,
        platform: str
    ) -> Optional[Event]:
        """Normalize raw extraction into Event object"""
        
        if not extraction_result.raw_data:
            logger.error("[Pipeline] No raw data to normalize")
            return None
        
        try:
            event = await gemini_normalizer.normalize(
                extraction_result.raw_data,
                url,
                platform
            )
            return event
            
        except Exception as e:
            logger.error(f"[Pipeline] Normalization failed: {e}")
            return None
    
    async def extract_batch(
        self, 
        urls: List[str],
        max_concurrent: int = 5
    ) -> List[Event]:
        """
        Extract multiple URLs with concurrency control
        
        Args:
            urls: List of URLs to extract
            max_concurrent: Maximum concurrent extractions
            
        Returns:
            List of successfully extracted Events
        """
        import asyncio
        
        logger.info(f"[Pipeline] Starting batch extraction: {len(urls)} URLs")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def extract_with_semaphore(url: str):
            async with semaphore:
                return await self.extract_event(url)
        
        tasks = [extract_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        events = [r for r in results if isinstance(r, Event)]
        
        logger.info(
            f"[Pipeline] Batch complete: {len(events)}/{len(urls)} successful"
        )
        
        return events


extraction_pipeline = ExtractionPipeline()
