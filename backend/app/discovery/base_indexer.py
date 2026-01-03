from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.shared.logger import logger


class BaseIndexer(ABC):
    """Abstract base class for platform indexers"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
    
    @abstractmethod
    async def discover_urls(
        self, 
        max_pages: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Discover event URLs from platform
        
        Args:
            max_pages: Maximum number of pages to crawl
            filters: Optional filters (e.g., category, date range)
            
        Returns:
            List of discovered event URLs
        """
        pass
    
    @abstractmethod
    async def is_event_url(self, url: str) -> bool:
        """
        Check if URL is an event page
        
        Args:
            url: URL to check
            
        Returns:
            True if URL is event page
        """
        pass
    
    async def discover_with_metadata(
        self,
        max_pages: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Discover URLs and return with metadata
        
        Returns:
            Dict with urls and metadata
        """
        logger.info(f"[{self.platform_name}] Starting URL discovery...")
        
        try:
            urls = await self.discover_urls(max_pages, filters)
            
            logger.info(
                f"[{self.platform_name}] Discovered {len(urls)} URLs"
            )
            
            return {
                "platform": self.platform_name,
                "urls": urls,
                "total_count": len(urls),
                "metadata": {
                    "max_pages": max_pages,
                    "filters": filters
                }
            }
            
        except Exception as e:
            logger.error(f"[{self.platform_name}] Discovery failed: {e}")
            raise
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify platform is accessible
        
        Returns:
            True if platform is accessible
        """
        pass
