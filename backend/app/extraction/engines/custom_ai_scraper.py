from typing import Dict, Any
import json
import re
from app.extraction.engines.base_engine import BaseEngine
from app.domain.extraction_result import ExtractionEngine
from app.shared.http_client import http_client, jina_reader
from app.shared.logger import logger
from app.config.gemini_config import get_gemini_model


class CustomAIScraper(BaseEngine):
    """Semantic AI scraper - extracts meaning, not just patterns"""
    
    def __init__(self):
        super().__init__(ExtractionEngine.CUSTOM_AI_SCRAPER)
        self.model = None
    
    def _get_model(self):
        """Lazy load Gemini model"""
        if self.model is None:
            self.model = get_gemini_model("models/gemini-2.5-flash")
        return self.model
    
    async def extract(self, url: str, platform: str) -> Dict[str, Any]:
        """Extract data using semantic understanding"""
        
        # Use Jina Reader for JavaScript-heavy sites
        if "unstop.com" in url or "devpost.com" in url:
            logger.info(f"[CustomAI] Using Jina Reader for JS rendering: {url}")
            html = await jina_reader.get(url)
        else:
            html = await http_client.get(url)
        
        # Send MORE context (Jina gives clean content, we can use more)
        html_content = html[:50000]
        
        prompt = self._build_semantic_prompt(html_content, url, platform)
        
        model = self._get_model()
        
        response = await self._generate_with_retry(model, prompt)
        
        try:
            extracted_data = self._parse_json_response(response.text)
            logger.info(f"[CustomAI] Semantically extracted data from {url}")
            return extracted_data
        except Exception as e:
            logger.warning(f"[CustomAI] Semantic extraction failed: {e}")
            return {
                "title": "",
                "description": "",
                "body_text": html_content,
                "url": url
            }
    
    def _build_semantic_prompt(self, html: str, url: str, platform: str) -> str:
        """Build semantic extraction prompt"""
        return f"""You are an intelligent web content extractor. Extract comprehensive event information with rich structured details.

**URL:** {url}
**Platform:** {platform}

**HTML Content:**
{html}

**Instructions:**
Extract ALL available information about this event. Look for:
- Event title and tagline
- "About the Event" section with detailed description
- Event flow, timeline, or phases
- How the competition/hackathon works
- Key highlights or features
- Judging criteria
- Deadlines and important dates
- Prizes and rewards
- Team size requirements
- Eligibility criteria
- Rules and guidelines
- Problem statements or themes
- All external links (registration, Discord, WhatsApp, etc.)

Return this EXACT JSON structure:

{{
  "title": "Full event title",
  "description": "One-line summary (max 150 chars)",
  "about": {{
    "overview": "Comprehensive paragraph describing the event in detail",
    "description_points": [
      "Key point 1 about what the event is",
      "Key point 2 about what participants will do",
      "Key point 3 about the format or structure"
    ],
    "event_flow": [
      "Step 1: Registration phase details",
      "Step 2: Competition/hackathon phases",
      "Step 3: Judging and winner selection"
    ],
    "how_it_works": [
      "Explanation of process step 1",
      "Explanation of process step 2"
    ],
    "key_highlights": [
      "Highlight 1 (e.g., prizes, networking)",
      "Highlight 2 (e.g., mentorship, workshops)"
    ],
    "judging_criteria": [
      "Criterion 1 (e.g., innovation)",
      "Criterion 2 (e.g., technical execution)"
    ]
  }},
  "deadlines": [
    {{"type": "registration", "date": "2024-01-15T23:59:59Z", "label": "Registration Closes"}},
    {{"type": "submission", "date": "2024-02-20T23:59:59Z", "label": "Project Submission"}}
  ],
  "prizes": [
    "1st Prize: ₹50,000 + Trophy",
    "2nd Prize: ₹25,000",
    "Participation certificates for all"
  ],
  "mode": "online",
  "location": "Online / City, Country",
  "organizer": {{
    "name": "Organization Name",
    "website": "https://...",
    "email": "contact@..."
  }},
  "team_size": {{
    "min": 1,
    "max": 4
  }},
  "eligibility": "Open to students and professionals worldwide",
  "rules": [
    "Rule 1: Original work only",
    "Rule 2: Code must be open source"
  ],
  "problem_statements": [
    "Theme 1: AI for Healthcare",
    "Theme 2: Fintech Innovation"
  ],
  "external_links": {{
    "website": "https://...",
    "registration": "https://...",
    "whatsapp": "https://chat.whatsapp.com/...",
    "discord": "https://discord.gg/...",
    "telegram": null,
    "linkedin": null,
    "twitter": null,
    "instagram": null
  }},
  "confidence_score": 0.9
}}

**CRITICAL RULES:**
- Extract ALL "About the Event" content into about.description_points as bullet points
- Extract "Event Flow" or "Timeline" into about.event_flow
- Look for sections like "Judging Criteria", "Key Highlights", "How it Works"
- description = ONE short sentence summary
- about.overview = full comprehensive paragraph
- Each array should contain ACTUAL extracted content, not generic placeholders
- If section doesn't exist, use empty array []
- Use null for missing individual fields
- Dates MUST be in ISO 8601 format
- mode MUST be exactly: "online", "offline", or "hybrid"
- confidence_score based on data completeness (0.0-1.0)

JSON:"""
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse JSON from Gemini response"""
        text = text.strip()
        
        # Remove markdown
        if "```json" in text:
            match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if match:
                text = match.group(1)
        elif "```" in text:
            match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
            if match:
                text = match.group(1)
        
        # Find JSON object
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
        
        # Fix trailing commas
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        
        return json.loads(text)
    
    async def _generate_with_retry(self, model, prompt: str, max_retries: int = 2):
        """Generate with retry"""
        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.15,  # Slightly increased for better content extraction
                        "top_p": 0.9,
                        "max_output_tokens": 8192,  # Increased for rich content
                        "response_mime_type": "application/json"
                    }
                )
                return response
            except Exception as e:
                logger.warning(f"[CustomAI] Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
        raise Exception("Max retries exceeded")
    
    def supports_url(self, url: str) -> bool:
        return True
    
    async def health_check(self) -> bool:
        try:
            model = self._get_model()
            test_response = model.generate_content("ping")
            return test_response is not None
        except Exception as e:
            logger.error(f"Custom AI scraper health check failed: {e}")
            return False
