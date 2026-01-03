from typing import Dict, Any
from app.extraction.engines.base_engine import BaseEngine
from app.domain.extraction_result import ExtractionEngine
from app.shared.logger import logger
from app.config.gemini_config import get_gemini_model


class GeminiGrounding(BaseEngine):
    """Engine C: Gemini with Google Search grounding (built-in browsing)"""
    
    def __init__(self):
        super().__init__(ExtractionEngine.GEMINI_GROUNDING)
        self.model = None
    
    def _get_model(self):
        """Lazy load Gemini model with grounding"""
        if self.model is None:
            self.model = get_gemini_model("models/gemini-2.5-flash")
        return self.model
    
    async def extract(self, url: str, platform: str) -> Dict[str, Any]:
        """Extract using Gemini's built-in web browsing capability"""
        
        prompt = f"""Visit this URL and extract comprehensive hackathon/competition information:
{url}

Provide detailed information about:
1. Event title and description
2. Registration and submission deadlines
3. Prizes and rewards
4. Event mode (online/offline/hybrid) and location
5. Organizer details
6. Team size requirements
7. Eligibility criteria
8. Rules and guidelines
9. Problem statements or themes
10. All external links (registration, website, Discord, WhatsApp, etc.)

Format your response as structured data with clear sections."""
        
        model = self._get_model()
        
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.2,
                    "max_output_tokens": 2048,
                }
            )
            
            extracted_text = response.text
            
            logger.info(f"[GeminiGrounding] Successfully extracted from {url}")
            
            return {
                "extracted_content": extracted_text,
                "url": url,
                "platform": platform,
                "extraction_method": "gemini_grounding"
            }
            
        except Exception as e:
            logger.error(f"[GeminiGrounding] Extraction failed: {e}")
            raise
    
    def supports_url(self, url: str) -> bool:
        """Gemini grounding supports all publicly accessible URLs"""
        return True
    
    async def health_check(self) -> bool:
        """Check if Gemini grounding is accessible"""
        try:
            model = self._get_model()
            test_response = model.generate_content("What is 2+2?")
            return test_response is not None
        except Exception as e:
            logger.error(f"Gemini grounding health check failed: {e}")
            return False
