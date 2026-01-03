from typing import Dict, Tuple
from app.shared.utils import extract_domain
from app.domain.platform import PlatformType, get_platform_by_domain
from app.shared.logger import logger


class URLClassifier:
    """Classifies URLs to determine extraction strategy"""
    
    CANONICAL_DOMAINS = {
        "devfolio.co": PlatformType.CANONICAL,
        "hack2skill.com": PlatformType.CANONICAL,
        "devnovate.com": PlatformType.CANONICAL,
    }
    
    INDEX_DOMAINS = {
        "unstop.com": PlatformType.INDEX,
        "devpost.com": PlatformType.INDEX,
    }
    
    def classify(self, url: str) -> Tuple[str, PlatformType]:
        """
        Classify URL and determine platform type
        
        Args:
            url: URL to classify
            
        Returns:
            Tuple of (platform_name, platform_type)
        """
        domain = extract_domain(url)
        
        platform = get_platform_by_domain(domain)
        
        if platform:
            logger.info(
                f"[Classifier] URL classified: {domain} -> "
                f"{platform.name} ({platform.platform_type.value})"
            )
            return platform.name, platform.platform_type
        
        logger.info(f"[Classifier] Unknown domain: {domain} -> treating as EXTERNAL")
        return "Unknown", PlatformType.EXTERNAL
    
    def should_deep_scrape(self, url: str) -> bool:
        """
        Determine if URL should be deeply scraped
        
        Canonical sources get deep scrape
        Index sources get light scrape + link following
        
        Args:
            url: URL to check
            
        Returns:
            True if should deep scrape
        """
        _, platform_type = self.classify(url)
        return platform_type == PlatformType.CANONICAL
    
    def needs_link_resolution(self, url: str) -> bool:
        """
        Check if URL needs external link resolution
        
        Index platforms need to follow links to find canonical source
        
        Args:
            url: URL to check
            
        Returns:
            True if needs link resolution
        """
        _, platform_type = self.classify(url)
        return platform_type == PlatformType.INDEX


url_classifier = URLClassifier()
