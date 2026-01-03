from typing import Dict, Any
import json
from app.extraction.engines.base_engine import BaseEngine
from app.domain.extraction_result import ExtractionEngine
from app.shared.http_client import http_client
from app.shared.logger import logger
from app.config.gemini_config import get_gemini_model


class CustomAIScraper(BaseEngine):
    """Engine D: Custom AI scraper using Gemini for intelligent extraction"""
    
    def __init__(self):
        super().__init__(ExtractionEngine.CUSTOM_AI_SCRAPER)
        self.model = None
    
    def _get_model(self):
        """Lazy load Gemini model"""
        if self.model is None:
            self.model = get_gemini_model("gemini-1.5-flash")
        return self.model
    
    async def extract(self, url: str, platform: str) -> Dict[str, Any]:
        """Extract data using Gemini AI"""
        
        html = await http_client.get(url)
        
        truncated_html = html[:15000]
        
        prompt = self._build_extraction_prompt(truncated_html, url, platform)
        
        model = self._get_model()
        
        response = await self._generate_with_retry(model, prompt)
        
        try:
            extracted_data = json.loads(response.text)
            logger.info(f"[CustomAI] Successfully extracted structured data from {url}")
            return extracted_data
        except json.JSONDecodeError as e:
            logger.warning(f"[CustomAI] Failed to parse JSON, returning raw text: {e}")
            return {
                "raw_extraction": response.text,
                "extraction_method": "fallback"
            }
    
    def _build_extraction_prompt(self, html: str, url: str, platform: str) -> str:
        """Build extraction prompt for Gemini"""
        return f"""You are an expert at extracting hackathon and competition information from HTML pages.

URL: {url}
Platform: {platform}

HTML Content (truncated):
{html}

Extract all relevant hackathon/competition information and return ONLY valid JSON with this exact structure:

{{
    "title": "event name",
    "description": "detailed description of the event",
    "deadlines": [
        {{"type": "registration", "date": "2024-01-15T23:59:59Z", "label": "Registration Deadline"}},
        {{"type": "submission", "date": "2024-02-20T23:59:59Z", "label": "Submission Deadline"}}
    ],
    "prizes": [
        "1st Prize: $10,000",
        "2nd Prize: $5,000"
    ],
    "mode": "online OR offline OR hybrid",
    "location": "city, country OR online",
    "organizer": {{
        "name": "Organizer name",
        "website": "https://organizer.com",
        "email": "contact@organizer.com"
    }},
    "team_size": {{
        "min": 1,
        "max": 4
    }},
    "eligibility": "who can participate",
    "rules": [
        "rule 1",
        "rule 2"
    ],
    "problem_statements": [
        "theme 1",
        "theme 2"
    ],
    "external_links": {{
        "registration": "https://register.com",
        "website": "https://event.com",
        "whatsapp": "https://chat.whatsapp.com/...",
        "discord": "https://discord.gg/...",
        "telegram": null
    }},
    "confidence_score": 0.85
}}

CRITICAL RULES:
1. Return ONLY the JSON object, no markdown formatting, no extra text
2. Use ISO 8601 format for all dates (YYYY-MM-DDTHH:MM:SSZ)
3. If information is missing, use null
4. Confidence score should be 0.0 to 1.0 based on data quality
5. Extract ALL links (registration, official website, social media)
6. Mode must be exactly: "online", "offline", or "hybrid"
7. Ensure the JSON is valid and parseable

Return the JSON now:"""
    
    async def _generate_with_retry(self, model, prompt: str, max_retries: int = 2):
        """Generate content with retry logic"""
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.1,
                        "top_p": 0.8,
                        "top_k": 40,
                        "max_output_tokens": 2048,
                    }
                )
                return response
            except Exception as e:
                logger.warning(f"[CustomAI] Generation attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
        
        raise Exception("Max retries exceeded for Gemini generation")
    
    def supports_url(self, url: str) -> bool:
        """Custom AI scraper supports all URLs"""
        return True
    
    async def health_check(self) -> bool:
        """Check if Gemini model is accessible"""
        try:
            model = self._get_model()
            test_response = model.generate_content("ping")
            return test_response is not None
        except Exception as e:
            logger.error(f"Custom AI scraper health check failed: {e}")
            return False
