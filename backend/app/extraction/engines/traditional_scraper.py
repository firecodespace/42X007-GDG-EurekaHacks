from typing import Dict, Any
from bs4 import BeautifulSoup
from app.extraction.engines.base_engine import BaseEngine
from app.domain.extraction_result import ExtractionEngine
from app.shared.http_client import http_client
from app.shared.logger import logger
from app.shared.utils import clean_text


class TraditionalScraper(BaseEngine):
    """Engine A: Traditional HTTP + BeautifulSoup scraper"""
    
    def __init__(self):
        super().__init__(ExtractionEngine.TRADITIONAL_SCRAPER)
    
    async def extract(self, url: str, platform: str) -> Dict[str, Any]:
        """Extract data using BeautifulSoup"""
        
        html = await http_client.get(url)
        soup = BeautifulSoup(html, 'lxml')
        
        raw_data = {
            "title": self._extract_title(soup),
            "description": self._extract_description(soup),
            "body_text": self._extract_body_text(soup),
            "links": self._extract_links(soup, url),
            "meta_tags": self._extract_meta_tags(soup),
            "html_length": len(html)
        }
        
        return raw_data
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tags = [
            soup.find('h1'),
            soup.find('title'),
            soup.find('meta', property='og:title')
        ]
        
        for tag in title_tags:
            if tag:
                if tag.name == 'meta':
                    return clean_text(tag.get('content', ''))
                return clean_text(tag.get_text())
        
        return ""
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description"""
        desc_selectors = [
            soup.find('meta', attrs={'name': 'description'}),
            soup.find('meta', property='og:description'),
            soup.find('p', class_='description'),
            soup.find('div', class_='description')
        ]
        
        for selector in desc_selectors:
            if selector:
                if selector.name == 'meta':
                    return clean_text(selector.get('content', ''))
                return clean_text(selector.get_text())
        
        paragraphs = soup.find_all('p', limit=3)
        if paragraphs:
            return ' '.join([clean_text(p.get_text()) for p in paragraphs])
        
        return ""
    
    def _extract_body_text(self, soup: BeautifulSoup) -> str:
        """Extract main body text"""
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        return clean_text(text)[:10000]
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, str]:
        """Extract important links"""
        links = {}
        
        keywords = {
            'register': ['register', 'registration', 'sign up', 'signup', 'apply'],
            'website': ['official website', 'website', 'visit site'],
            'whatsapp': ['whatsapp', 'whatsapp group'],
            'discord': ['discord', 'discord server'],
            'telegram': ['telegram'],
        }
        
        for a_tag in soup.find_all('a', href=True):
            text = clean_text(a_tag.get_text()).lower()
            href = a_tag.get('href', '')
            
            for link_type, search_terms in keywords.items():
                if any(term in text for term in search_terms):
                    if link_type not in links:
                        links[link_type] = href
        
        return links
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meta tags"""
        meta_tags = {}
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            
            if name and content:
                meta_tags[name] = content
        
        return meta_tags
    
    def supports_url(self, url: str) -> bool:
        """Traditional scraper supports all URLs"""
        return True
    
    async def health_check(self) -> bool:
        """Check if HTTP client is working"""
        try:
            await http_client.get("https://httpbin.org/status/200")
            return True
        except Exception as e:
            logger.error(f"Traditional scraper health check failed: {e}")
            return False
