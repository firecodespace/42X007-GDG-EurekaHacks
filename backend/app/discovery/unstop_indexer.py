from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import re
from app.discovery.base_indexer import BaseIndexer
from app.shared.http_client import http_client
from app.shared.logger import logger
from app.shared.utils import is_valid_url


class UnstopIndexer(BaseIndexer):
    """Indexer for Unstop platform"""
    
    BASE_URL = "https://unstop.com"
    COMPETITIONS_URL = f"{BASE_URL}/competitions"
    HACKATHONS_URL = f"{BASE_URL}/hackathons"
    
    def __init__(self):
        super().__init__("Unstop")
    
    async def discover_urls(
        self,
        max_pages: Optional[int] = 3,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Discover hackathon URLs from Unstop"""
        
        discovered_urls = set()
        
        search_urls = [self.HACKATHONS_URL, self.COMPETITIONS_URL]
        
        for search_url in search_urls:
            urls = await self._scrape_listing_page(search_url, max_pages)
            discovered_urls.update(urls)
        
        return list(discovered_urls)
    
    async def _scrape_listing_page(
        self, 
        base_url: str, 
        max_pages: Optional[int]
    ) -> List[str]:
        """Scrape listing pages for event URLs using Jina Reader"""
        urls = []
        
        try:
            for page in range(1, (max_pages or 3) + 1):
                page_url = f"{base_url}?page={page}" if page > 1 else base_url
                
                logger.info(f"[Unstop] Scraping page {page}: {page_url}")
                
                # Use Jina Reader to render JavaScript
                jina_url = f"https://r.jina.ai/{page_url}"
                html = await http_client.get(jina_url)
                
                # Extract URLs from rendered content
                page_urls = self._extract_event_urls_from_text(html)
                
                # Also try traditional parsing as fallback
                soup = BeautifulSoup(html, 'lxml')
                traditional_urls = self._extract_event_urls(soup)
                
                # Combine both methods
                all_urls = list(set(page_urls + traditional_urls))
                urls.extend(all_urls)
                
                logger.info(f"[Unstop] Found {len(all_urls)} URLs on page {page}")
                
                if not all_urls:
                    logger.info(f"[Unstop] No more URLs found, stopping pagination")
                    break
                
        except Exception as e:
            logger.error(f"[Unstop] Error scraping listing page: {e}")
        
        return urls
    
    def _extract_event_urls_from_text(self, text: str) -> List[str]:
        """Extract URLs from rendered text content"""
        urls = []
        
        # Look for Unstop event URLs in the text
        patterns = [
            r'https://unstop\.com/competitions/[a-zA-Z0-9\-]+\-\d+',
            r'https://unstop\.com/hackathons/[a-zA-Z0-9\-]+\-\d+',
            r'unstop\.com/competitions/[a-zA-Z0-9\-]+\-\d+',
            r'unstop\.com/hackathons/[a-zA-Z0-9\-]+\-\d+'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if not match.startswith('http'):
                    match = f"https://{match}"
                if self._is_valid_event_url(match):
                    urls.append(match)
        
        return list(set(urls))
    
    def _extract_event_urls(self, soup: BeautifulSoup) -> List[str]:
        """Extract event URLs from HTML soup (traditional method)"""
        urls = []
        
        event_link_patterns = [
            r'/competitions/[a-zA-Z0-9\-]+\-\d+',
            r'/hackathons/[a-zA-Z0-9\-]+\-\d+'
        ]
        
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            
            if href.startswith('/'):
                href = self.BASE_URL + href
            
            for pattern in event_link_patterns:
                if re.search(pattern, href):
                    if self._is_valid_event_url(href):
                        urls.append(href)
                        break
        
        return list(set(urls))
    
    def _is_valid_event_url(self, url: str) -> bool:
        """Validate if URL is a proper event page"""
        if not is_valid_url(url):
            return False
        
        # Must have numeric ID at the end
        if not re.search(r'\-\d+$', url):
            return False
        
        excluded_patterns = [
            '/apply',
            '/register',
            '/login',
            '/signup',
            '/profile',
            '/search',
            '/filter',
            '?page=',
            '/user/',
            '/organisation/'
        ]
        
        for pattern in excluded_patterns:
            if pattern in url:
                return False
        
        return True
    
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
