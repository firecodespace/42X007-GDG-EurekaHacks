from typing import List, Dict, Any, Optional
import re
from app.discovery.base_indexer import BaseIndexer
from app.shared.http_client import http_client
from app.shared.logger import logger


class UnstopIndexer(BaseIndexer):
    """Indexer for Unstop platform using their API"""
    
    BASE_URL = "https://unstop.com"
    API_URL = "https://unstop.com/api/public/opportunity/search-result"
    
    def __init__(self):
        super().__init__("Unstop")
    
    async def discover_urls(
        self,
        max_pages: Optional[int] = 3,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Discover hackathon URLs from Unstop API"""
        
        discovered_urls = set()
        
        # Search for hackathons and competitions
        categories = ["hackathons", "competitions"]
        
        for category in categories:
            urls = await self._fetch_from_api(category, max_pages)
            discovered_urls.update(urls)
        
        return list(discovered_urls)
    
    async def _fetch_from_api(
        self, 
        category: str, 
        max_pages: Optional[int]
    ) -> List[str]:
        """Fetch events from Unstop API"""
        urls = []
        
        try:
            for page in range(1, (max_pages or 3) + 1):
                logger.info(f"[Unstop] Fetching {category} page {page} from API")
                
                # Unstop API payload
                payload = {
                    "opportunity": category,
                    "page": page,
                    "size": 20,
                    "filters": {
                        "status": ["open"],
                        "type": ["public"]
                    }
                }
                
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Origin": "https://unstop.com",
                    "Referer": f"https://unstop.com/{category}"
                }
                
                # Make API request
                response = await http_client.post(
                    self.API_URL,
                    json=payload,
                    headers=headers
                )
                
                # Parse JSON response
                import json
                data = json.loads(response)
                
                items = data.get("data", {}).get("data", [])
                
                logger.info(f"[Unstop] Found {len(items)} items on page {page}")
                
                if not items:
                    break
                
                # Extract URLs
                for item in items:
                    # Build URL from item data
                    slug = item.get("public_url", "")
                    regnumber = item.get("regnumber", "")
                    
                    if slug and regnumber:
                        url = f"{self.BASE_URL}/{category}/{slug}-{regnumber}"
                        urls.append(url)
                
        except Exception as e:
            logger.error(f"[Unstop] Error fetching from API: {e}")
        
        return list(set(urls))
    
    async def is_event_url(self, url: str) -> bool:
        """Check if URL is an Unstop event page"""
        event_patterns = [
            r'unstop\.com/competitions/[a-zA-Z0-9\-]+\-\d+',
            r'unstop\.com/hackathons/[a-zA-Z0-9\-]+\-\d+'
        ]
        
        for pattern in event_patterns:
            if re.search(pattern, url):
                return True
        
        return False
    
    async def health_check(self) -> bool:
        """Check if Unstop is accessible"""
        try:
            html = await http_client.get(self.BASE_URL)
            return "unstop" in html.lower()
        except Exception as e:
            logger.error(f"[Unstop] Health check failed: {e}")
            return False
