from typing import List, Dict, Any, Optional
import re
import asyncio
from app.discovery.base_indexer import BaseIndexer
from app.shared.logger import logger


class UnstopIndexer(BaseIndexer):
    """Indexer for Unstop using Selenium (bypasses bot detection)"""
    
    BASE_URL = "https://unstop.com"
    
    def __init__(self):
        super().__init__("Unstop")
    
    async def discover_urls(
        self,
        max_pages: Optional[int] = 3,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Discover hackathon URLs from Unstop"""
        
        # Run selenium in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        urls = await loop.run_in_executor(None, self._scrape_with_selenium, max_pages)
        
        return urls
    
    def _scrape_with_selenium(self, max_pages: int) -> List[str]:
        """Scrape using Selenium"""
        import undetected_chromedriver as uc
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        
        urls = set()
        
        try:
            logger.info("[Unstop] Launching browser...")
            
            options = uc.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = uc.Chrome(options=options)
            
            categories = ["/hackathons", "/competitions"]
            
            for category in categories:
                try:
                    url = f"{self.BASE_URL}{category}"
                    logger.info(f"[Unstop] Scraping: {url}")
                    
                    driver.get(url)
                    
                    # Wait for content to load
                    time.sleep(3)
                    
                    # Scroll to load more
                    for _ in range(3):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                    
                    # Extract all links
                    page_html = driver.page_source
                    
                    # Find event URLs
                    pattern = rf'{self.BASE_URL}{category}/[a-zA-Z0-9\-]+\-\d+'
                    found_urls = re.findall(pattern, page_html)
                    
                    urls.update(found_urls)
                    
                    logger.info(f"[Unstop] Found {len(found_urls)} URLs in {category}")
                    
                except Exception as e:
                    logger.error(f"[Unstop] Error scraping {category}: {e}")
            
            driver.quit()
            
        except Exception as e:
            logger.error(f"[Unstop] Selenium error: {e}")
        
        return list(urls)
    
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
        from app.shared.http_client import http_client
        try:
            html = await http_client.get(self.BASE_URL)
            return "unstop" in html.lower()
        except Exception as e:
            logger.error(f"[Unstop] Health check failed: {e}")
            return False
