from typing import Dict, Any, Optional
import json
import re
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
            self.model = get_gemini_model("models/gemini-2.5-flash")
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
            
            logger.info(f"[Normalizer] Sending to Gemini...")
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.05,
                    "top_p": 0.8,
                    "max_output_tokens": 4096,
                    "response_mime_type": "application/json"
                }
            )
            
            # DEBUG: Log raw response
            logger.info(f"[Normalizer] Raw Gemini response length: {len(response.text) if response.text else 0}")
            logger.debug(f"[Normalizer] Full Gemini response: {response.text}")
            
            if not response.text:
                logger.error(f"[Normalizer] Gemini returned empty response")
                return None
            
            normalized_json = self._parse_response(response.text)
            
            if not normalized_json:
                logger.warning(f"[Normalizer] Failed to parse response for {source_url}")
                return None
            
            # Apply defaults for None values
            normalized_json = self._apply_defaults(normalized_json)
            
            normalized_json["source_url"] = source_url
            normalized_json["source_platform"] = source_platform
            normalized_json["raw_data"] = raw_data
            
            event = Event(**normalized_json)
            
            logger.info(f"[Normalizer] Successfully normalized: {event.title}")
            
            return event
            
        except Exception as e:
            logger.error(f"[Normalizer] Normalization failed: {e}", exc_info=True)
            return None
    
    def _apply_defaults(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values for required fields that are None"""
        
        # Title - absolutely required
        if not data.get("title"):
            data["title"] = "Untitled Event"
        
        # Description - required string
        if not data.get("description"):
            data["description"] = data.get("title", "No description available")
        
        # Mode - required enum
        if not data.get("mode"):
            data["mode"] = "online"
        
        # Team size - required object with nested values
        if not data.get("team_size") or data.get("team_size") is None:
            data["team_size"] = {"min": 1, "max": 4}
        else:
            # Ensure nested fields exist
            if data["team_size"].get("min") is None:
                data["team_size"]["min"] = 1
            if data["team_size"].get("max") is None:
                data["team_size"]["max"] = 4
        
        # Organizer - ensure it's a dict with required name
        if not data.get("organizer") or data.get("organizer") is None:
            data["organizer"] = {"name": "Unknown", "website": None, "email": None}
        else:
            if not data["organizer"].get("name"):
                data["organizer"]["name"] = "Unknown"
            if "website" not in data["organizer"]:
                data["organizer"]["website"] = None
            if "email" not in data["organizer"]:
                data["organizer"]["email"] = None
        
        # External links - ensure it's a dict
        if not data.get("external_links"):
            data["external_links"] = {}
        
        # Deadlines - ensure it's a list
        if not data.get("deadlines"):
            data["deadlines"] = []
        
        # Prizes - ensure it's a list
        if not data.get("prizes"):
            data["prizes"] = []
        
        # Rules - ensure it's a list
        if not data.get("rules"):
            data["rules"] = []
        
        # Problem statements - ensure it's a list
        if not data.get("problem_statements"):
            data["problem_statements"] = []
        
        # Location
        if not data.get("location"):
            data["location"] = "To be announced"
        
        # Eligibility
        if not data.get("eligibility"):
            data["eligibility"] = "Open to all"
        
        # About
        if not data.get("about"):
            data["about"] = {
                "overview": data.get("description", "No detailed information available"),
                "description_points": [],
                "event_flow": [],
                "how_it_works": [],
                "key_highlights": [],
                "judging_criteria": []
            }        
            
        # Confidence score
        if data.get("confidence_score") is None:
            data["confidence_score"] = 0.5

        
        logger.debug(f"[Normalizer] After applying defaults: title={data.get('title')}, organizer.name={data.get('organizer', {}).get('name')}")
        
        return data
    
    def _build_normalization_prompt(
        self,
        raw_data: Dict[str, Any],
        source_url: str
    ) -> str:
        """Build normalization prompt"""
        
        # Extract useful content from raw_data
        content = ""
        if "body_text" in raw_data:
            content = raw_data["body_text"][:8000]  # Reduced to leave room for output
        elif "description" in raw_data:
            content = str(raw_data.get("description", ""))
        else:
            content = json.dumps(raw_data, indent=2, default=str)[:8000]
        
        return f"""Extract event info as compact JSON.

    URL: {source_url}

    Content:
    {content}

    Return this JSON structure (keep it compact):
    {{
    "title": "event name",
    "description": "brief description (max 100 chars)",
    "deadlines": [],
    "prizes": [],
    "mode": "online",
    "location": "city or online",
    "organizer": {{"name": "org", "website": null, "email": null}},
    "team_size": {{"min": 1, "max": 4}},
    "eligibility": "who can join",
    "rules": [],
    "problem_statements": [],
    "external_links": {{}},
    "confidence_score": 0.8
    }}

    Rules:
    - Keep description under 100 characters
    - Use null for missing data
    - mode: "online", "offline", or "hybrid"
    - Return ONLY compact JSON

    JSON:"""

    
    def _parse_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse Gemini response to JSON with aggressive repair"""
        try:
            if not response_text:
                logger.error("[Normalizer] Empty response text")
                return None
            
            original_text = response_text
            response_text = response_text.strip()
            
            logger.debug(f"[Normalizer] Raw response (first 500): {response_text[:500]}")
            
            # Remove markdown code blocks
            if "```json" in response_text:
                match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
                if match:
                    response_text = match.group(1).strip()
                else:
                    start = response_text.find("```json")
                    if start != -1:
                        response_text = response_text[start + 7:].strip()
                        if response_text.endswith("```"):
                            response_text = response_text[:-3].strip()
            elif "```" in response_text:
                match = re.search(r'```\s*(.*?)\s*```', response_text, re.DOTALL)
                if match:
                    response_text = match.group(1).strip()
            
            # Remove any remaining backticks
            response_text = response_text.strip('`').strip()
            if response_text.startswith("json"):
                response_text = response_text[4:].strip()
            
            # Try direct parse with strict=False
            try:
                parsed = json.loads(response_text, strict=False)
                logger.info(f"[Normalizer] Successfully parsed JSON with {len(parsed)} fields")
                return parsed
            except json.JSONDecodeError as first_error:
                logger.debug(f"[Normalizer] First parse failed: {first_error}")
            
            # Repair common issues
            response_text = re.sub(r',\s*}', '}', response_text)
            response_text = re.sub(r',\s*]', ']', response_text)
            
            # Try again after repair
            try:
                parsed = json.loads(response_text, strict=False)
                logger.info(f"[Normalizer] Parsed after repair with {len(parsed)} fields")
                return parsed
            except json.JSONDecodeError as e:
                logger.error(f"[Normalizer] JSON parse error: {e}")
                logger.error(f"[Normalizer] Problematic JSON: {response_text[:1000]}")
                return None
            
        except Exception as e:
            logger.error(f"[Normalizer] Unexpected error: {e}")
            logger.error(f"[Normalizer] Original: {original_text[:1000]}")
            return None


gemini_normalizer = GeminiNormalizer()
