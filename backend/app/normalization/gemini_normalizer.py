from typing import Dict, Any, Optional
import json
from app.config.gemini_config import get_gemini_model
from app.domain.event import Event
from app.shared.logger import logger


class GeminiNormalizer:
    """Normalize raw extraction data using Gemini AI"""
    
    def __init__(self):
        self.model = None
    
    def _get_model(self):
        """Lazy load Gemini model"""
        if self.model is None:
            self.model = get_gemini_model("gemini-1.5-flash")
        return self.model
    
    async def normalize(
        self,
        raw_data: Dict[str, Any],
        source_url: str,
        source_platform: str
    ) -> Optional[Event]:
        """
        Normalize raw extracted data into Event model
        
        Args:
            raw_data: Raw extracted data from engines
            source_url: Original URL
            source_platform: Platform name
            
        Returns:
            Normalized Event object or None if normalization fails
        """
        try:
            prompt = self._build_normalization_prompt(raw_data, source_url)
            
            model = self._get_model()
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "top_p": 0.8,
                    "max_output_tokens": 2048,
                }
            )
            
            normalized_json = self._parse_response(response.text)
            
            if not normalized_json:
                logger.warning(f"[Normalizer] Failed to parse response for {source_url}")
                return None
            
            normalized_json["source_url"] = source_url
            normalized_json["source_platform"] = source_platform
            normalized_json["raw_data"] = raw_data
            
            event = Event(**normalized_json)
            
            logger.info(f"[Normalizer] Successfully normalized: {event.title}")
            
            return event
            
        except Exception as e:
            logger.error(f"[Normalizer] Normalization failed: {e}")
            return None
    
    def _build_normalization_prompt(
        self,
        raw_data: Dict[str, Any],
        source_url: str
    ) -> str:
        """Build normalization prompt"""
        return f"""You are a data normalization expert. Convert this raw scraped data into a clean, structured JSON format.

Source URL: {source_url}

Raw Data:
{json.dumps(raw_data, indent=2, default=str)}

Convert this into the following JSON structure. Extract and infer information intelligently:

{{
    "title": "event name",
    "description": "comprehensive event description",
    "deadlines": [
        {{"type": "registration", "date": "2024-01-15T23:59:59Z", "label": "Registration Deadline"}},
        {{"type": "submission", "date": "2024-02-20T23:59:59Z", "label": "Submission Deadline"}},
        {{"type": "event_start", "date": "2024-02-01T09:00:00Z", "label": "Event Start"}},
        {{"type": "event_end", "date": "2024-02-03T18:00:00Z", "label": "Event End"}}
    ],
    "mode": "online OR offline OR hybrid",
    "location": "city, country OR online",
    "organizer": {{
        "name": "organizer name",
        "website": "https://organizer.com",
        "email": "contact@organizer.com",
        "logo": null
    }},
    "prizes": [
        "1st Prize: $10,000",
        "2nd Prize: $5,000",
        "3rd Prize: $2,000"
    ],
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
        "theme 1: description",
        "theme 2: description"
    ],
    "external_links": {{
        "website": "https://event.com",
        "registration": "https://register.com",
        "whatsapp": "https://chat.whatsapp.com/...",
        "discord": "https://discord.gg/...",
        "telegram": null,
        "linkedin": null,
        "twitter": null,
        "instagram": null
    }},
    "confidence_score": 0.85
}}

CRITICAL RULES:
1. Return ONLY valid JSON, no markdown, no extra text
2. Dates must be ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
3. If information missing, use null (not empty string)
4. Mode must be exactly: "online", "offline", or "hybrid"
5. Confidence score 0.0-1.0 based on data completeness and quality
6. Extract ALL available links
7. Infer information intelligently from context

Return JSON now:"""
    
    def _parse_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse Gemini response to JSON"""
        try:
            response_text = response_text.strip()
            
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            logger.error(f"[Normalizer] JSON parse error: {e}")
            logger.debug(f"[Normalizer] Raw response: {response_text[:500]}")
            return None


gemini_normalizer = GeminiNormalizer()
