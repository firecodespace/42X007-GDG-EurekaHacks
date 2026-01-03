from typing import List, Dict, Optional
from app.domain.extraction_result import ExtractionEngine
from app.shared.utils import extract_domain
from app.shared.logger import logger


class StrategyRouter:
    """Intelligent routing system for selecting extraction engines"""
    
    STRATEGY_RULES: Dict[str, List[str]] = {
        "devfolio.co": ["traditional_scraper", "custom_ai_scraper"],
        "hack2skill.com": ["traditional_scraper", "custom_ai_scraper"],
        "devnovate.com": ["traditional_scraper", "custom_ai_scraper"],
        "unstop.com": ["custom_ai_scraper", "traditional_scraper"],  # Custom AI uses Jina!
        "devpost.com": ["custom_ai_scraper", "traditional_scraper"],
        "notion.so": ["custom_ai_scraper", "traditional_scraper"],
        "github.com": ["traditional_scraper", "custom_ai_scraper"],
        "default": ["traditional_scraper", "custom_ai_scraper"]
    }




    
    ENGINE_MAPPING = {
        "traditional_scraper": ExtractionEngine.TRADITIONAL_SCRAPER,
        "custom_ai_scraper": ExtractionEngine.CUSTOM_AI_SCRAPER,
        "gemini_grounding": ExtractionEngine.GEMINI_GROUNDING,
    }
    
    def select_strategy(self, url: str) -> List[ExtractionEngine]:
        """
        Select ordered list of engines to try for given URL
        
        Args:
            url: URL to extract from
            
        Returns:
            List of ExtractionEngine enums in priority order
        """
        domain = extract_domain(url)
        
        strategy_names = self.STRATEGY_RULES.get(
            domain, 
            self.STRATEGY_RULES["default"]
        )
        
        engines = [
            self.ENGINE_MAPPING[name] 
            for name in strategy_names 
            if name in self.ENGINE_MAPPING
        ]
        
        logger.info(f"Selected strategy for {domain}: {[e.value for e in engines]}")
        
        return engines
    
    def get_primary_engine(self, url: str) -> ExtractionEngine:
        """Get the primary (first) engine for URL"""
        strategies = self.select_strategy(url)
        return strategies[0] if strategies else ExtractionEngine.CUSTOM_AI_SCRAPER
    
    def add_custom_rule(self, domain: str, engines: List[str]) -> None:
        """Add custom routing rule for domain"""
        self.STRATEGY_RULES[domain] = engines
        logger.info(f"Added custom rule for {domain}: {engines}")


strategy_router = StrategyRouter()
