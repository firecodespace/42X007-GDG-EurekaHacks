import json
from typing import Dict, Any
from app.models.user_profile import UserProfile
from app.domain.event import Event
from app.config.gemini_config import get_gemini_model
from app.services.recommendation_cache import recommendation_cache
from app.shared.logger import logger


class PersonalizationService:
    """AI-powered event personalization"""
    
    def __init__(self):
        self.model = get_gemini_model()
    
    async def personalize_event(
        self, 
        event: Event, 
        user_profile: UserProfile,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Generate personalized event description using Gemini"""
        
        try:
            event_id = event.id
            
            # Check cache first
            if use_cache:
                cached = await recommendation_cache.get_cached(user_profile.user_id, event_id)
                if cached:
                    logger.info(f"[Personalization] ⚡ Using cached for: {event_id}")
                    enhanced_event = event.dict()
                    enhanced_event["personalization"] = cached
                    return enhanced_event
            
            logger.info(f"[Personalization] Starting for event: {event.title}")
            
            # Build context-rich prompt
            prompt = self._build_personalization_prompt(event, user_profile)
            
            logger.info(f"[Personalization] Calling Gemini API...")
            
            # Call Gemini API with strict JSON output
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 2048,
                }
            )
            
            logger.info(f"[Personalization] Received response from Gemini")
            logger.info(f"[Personalization] Response text length: {len(response.text)}")
            
            # Parse JSON response
            personalized_data = self._parse_gemini_response(response.text)
            
            # Cache the result (only if no error)
            if "error" not in personalized_data:
                await recommendation_cache.set_cached(
                    user_profile.user_id, 
                    event_id, 
                    personalized_data
                )
            
            # Merge with original event data
            enhanced_event = event.dict()
            enhanced_event["personalization"] = personalized_data
            
            logger.info(f"[Personalization] ✅ Successfully generated for: {event.title}")
            logger.info(f"[Personalization] Match score: {personalized_data.get('match_score', 'N/A')}")
            
            return enhanced_event
            
        except Exception as e:
            logger.error(f"[Personalization] ❌ Error: {e}", exc_info=True)
            
            # Return event with fallback personalization
            enhanced_event = event.dict()
            enhanced_event["personalization"] = self._get_fallback_personalization(str(e))
            return enhanced_event
    
    def _build_personalization_prompt(
        self, 
        event: Event, 
        user_profile: UserProfile
    ) -> str:
        """Build AI prompt with event + user context"""
        
        # Extract user context
        user_skills = ", ".join(user_profile.skills[:5]) if user_profile.skills else "None"
        user_interests = ", ".join(user_profile.interests[:5]) if user_profile.interests else "None"
        user_experience = user_profile.experience_level
        
        # Extract event context (simplified)
        event_title = event.title
        event_desc = event.description[:300] if event.description else "No description"
        event_org = event.organizer.name if event.organizer else "Unknown"
        event_mode = event.mode
        
        prompt = f"""You are a JSON API. Return ONLY valid JSON with NO markdown, NO explanations, NO code blocks.

EVENT:
Title: {event_title}
Description: {event_desc}
Organizer: {event_org}
Mode: {event_mode}

USER:
Skills: {user_skills}
Interests: {user_interests}
Experience: {user_experience}

Return this EXACT JSON structure (replace placeholder text with real content):
{{
  "personalized_description": "Write 100-150 words explaining why this event fits this specific user based on their skills and interests",
  "why_you_should_participate": "Write 80-100 words on concrete benefits for THIS user",
  "skills_you_will_learn": ["specific_skill_1", "specific_skill_2", "specific_skill_3", "specific_skill_4", "specific_skill_5"],
  "skills_required": [{{"skill": "example_skill", "user_has": true}}],
  "match_score": 85,
  "personalized_tips": ["actionable_tip_1", "actionable_tip_2", "actionable_tip_3"],
  "challenge_level": "perfect-fit",
  "networking_opportunities": "One sentence about who they will meet"
}}

CRITICAL RULES:
1. Return ONLY the JSON object
2. NO ``` markers
3. NO "json" label
4. NO explanatory text
5. Ensure all strings are properly quoted
6. Match score must be 0-100
7. Challenge level must be: "perfect-fit" OR "slight-stretch" OR "ambitious"

START JSON NOW:"""
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's JSON response with robust error handling"""
        
        try:
            # Clean response aggressively
            cleaned = response_text.strip()
            
            # Remove markdown code blocks
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            # Find JSON boundaries
            start = cleaned.find('{')
            end = cleaned.rfind('}')
            
            if start != -1 and end != -1:
                cleaned = cleaned[start:end+1]
            
            logger.info(f"[Personalization] Attempting parse: {cleaned[:200]}...")
            
            # Parse JSON
            parsed = json.loads(cleaned)
            
            # Validate and fill missing fields
            required_fields = {
                "personalized_description": "This event aligns with your profile.",
                "why_you_should_participate": "Great opportunity to apply your skills.",
                "skills_you_will_learn": ["Problem solving", "Team collaboration", "Critical thinking"],
                "skills_required": [],
                "match_score": 50,
                "personalized_tips": ["Prepare thoroughly", "Network actively", "Showcase your skills"],
                "challenge_level": "moderate",
                "networking_opportunities": "Connect with peers and professionals"
            }
            
            for field, default in required_fields.items():
                if field not in parsed or parsed[field] is None:
                    logger.warning(f"[Personalization] Missing field '{field}', using default")
                    parsed[field] = default
            
            # Validate match_score range
            if not isinstance(parsed["match_score"], (int, float)) or not (0 <= parsed["match_score"] <= 100):
                parsed["match_score"] = 50
            
            # Validate challenge_level
            valid_levels = ["perfect-fit", "slight-stretch", "ambitious", "moderate"]
            if parsed["challenge_level"] not in valid_levels:
                parsed["challenge_level"] = "moderate"
            
            logger.info(f"[Personalization] ✅ Successfully parsed and validated JSON")
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"[Personalization] ❌ JSON parse error: {e}")
            logger.error(f"[Personalization] Raw response (first 500 chars): {response_text[:500]}")
            
            return self._get_fallback_personalization(f"JSON parse error: {str(e)}")
    
    def _get_fallback_personalization(self, error_msg: str = "") -> Dict[str, Any]:
        """Return safe fallback personalization when AI fails"""
        return {
            "personalized_description": "This competition offers an excellent opportunity to apply your technical skills in a practical, real-world setting. The challenge aligns with your background and provides a platform to showcase your abilities while learning from peers.",
            "why_you_should_participate": "Participating will help you gain hands-on experience, expand your professional network, and add a valuable achievement to your portfolio. The competition format encourages creative problem-solving and collaborative teamwork.",
            "skills_you_will_learn": [
                "Problem solving",
                "Team collaboration", 
                "Critical thinking",
                "Presentation skills",
                "Strategic planning"
            ],
            "skills_required": [
                {"skill": "Analytical thinking", "user_has": True},
                {"skill": "Communication", "user_has": False}
            ],
            "match_score": 50,
            "personalized_tips": [
                "Research the problem statement thoroughly before starting",
                "Form a diverse team with complementary skills",
                "Practice your presentation to communicate ideas clearly"
            ],
            "challenge_level": "moderate",
            "networking_opportunities": "Connect with fellow participants, industry mentors, and potential collaborators in your field",
            "error": error_msg if error_msg else None
        }


personalization_service = PersonalizationService()
