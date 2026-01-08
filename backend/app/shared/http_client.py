import httpx
from typing import Optional, Dict, Any
from app.config.settings import settings
from app.shared.logger import logger
from app.shared.exceptions import ScraperError
from tenacity import retry, stop_after_attempt, wait_exponential


class HTTPClient:
    """Async HTTP client with retry logic"""
    
    def __init__(self):
        self.timeout = settings.request_timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    @retry(
        stop=stop_after_attempt(settings.retry_max_attempts),
        wait=wait_exponential(multiplier=settings.retry_backoff_factor, min=1, max=10)
    )
    async def get(
        self, 
        url: str, 
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        """GET request with retry logic"""
        try:
            request_headers = {**self.headers, **(headers or {})}
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=request_headers, params=params)
                response.raise_for_status()
                
                logger.info(f"Successfully fetched: {url}")
                return response.text
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching {url}: {e}")
            raise ScraperError(f"Failed to fetch {url}: {e.response.status_code}")
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching {url}")
            raise ScraperError(f"Timeout while fetching {url}")
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")
            raise ScraperError(f"Failed to fetch {url}: {str(e)}")
    
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> str:
        """POST request"""
        try:
            request_headers = {**self.headers, **(headers or {})}
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url, 
                    data=data, 
                    json=json, 
                    headers=request_headers
                )
                response.raise_for_status()
                
                logger.info(f"Successfully posted to: {url}")
                return response.text
                
        except Exception as e:
            logger.error(f"POST error to {url}: {e}")
            raise ScraperError(f"Failed to POST to {url}: {str(e)}")


http_client = HTTPClient()


class JinaReaderClient:
    """Use Jina AI Reader for JavaScript-heavy sites"""
    
    BASE_URL = "https://r.jina.ai/"
    
    async def get(self, url: str) -> str:
        """
        Fetch URL using Jina Reader (handles JS rendering)
        
        Args:
            url: URL to fetch
            
        Returns:
            Clean, readable content
        """
        try:
            jina_url = f"{self.BASE_URL}{url}"
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(jina_url)
                response.raise_for_status()
                
                content = response.text
                logger.info(f"Successfully fetched with Jina Reader: {url}")
                return content
                
        except Exception as e:
            logger.error(f"Jina Reader fetch failed for {url}: {e}")
            raise ScraperError(f"Failed to fetch {url} with Jina Reader: {e}")


jina_reader = JinaReaderClient()
