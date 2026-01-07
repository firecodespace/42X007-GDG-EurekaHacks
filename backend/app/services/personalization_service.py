import json
from typing import Dict, Any
from app.models.user_profile import UserProfile
from app.domain.event import Event
from app.config.gemini_config import get_gemini_model
from app.shared.logger import logger


class PersonalizationService:
    """AI-powered event personalization"""
    
    def __init__(self):
        self.model = get_gemini_model()
    
    async def personalize_event(
        self, 
        event: Event, 
        user_profile: UserProfile
    ) -> Dict[str, Any]:
        """Generate personalized event description using Gemini"""
        
        try:
            logger.info(f"[Personalization] Starting for event: {event.title}")
            
            # Build context-rich prompt
            prompt = self._build_personalization_prompt(event, user_profile)
            
            logger.info(f"[Personalization] Calling Gemini API...")
            
            # Call Gemini API with timeout
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
            
            # Merge with original event data
            enhanced_event = event.dict()
            enhanced_event["personalization"] = personalized_data
            
            logger.info(f"[Personalization] ✅ Successfully generated for: {event.title}")
            logger.info(f"[Personalization] Match score: {personalized_data.get('match_score', 'N/A')}")
            
            return enhanced_event
            
        except Exception as e:
            logger.error(f"[Personalization] ❌ Error: {e}", exc_info=True)
            
            # Return event with error personalization
            enhanced_event = event.dict()
            enhanced_event["personalization"] = {
                "error": str(e),
                "personalized_description": "Unable to generate personalization at this time.",
                "match_score": 50
            }
            return enhanced_event
    
    def _build_personalization_prompt(
        self, 
        event: Event, 
        user_profile: UserProfile
    ) -> str:
        """Build AI prompt with event + user context"""
        
        # Extract user context
        user_skills = ", ".join(user_profile.skills) if user_profile.skills else "None"
        user_interests = ", ".join(user_profile.interests) if user_profile.interests else "None"
        user_experience = user_profile.experience_level
        
        # Extract event context (simplified to avoid token limits)
        event_summary = {
            "title": event.title,
            "description": event.description,
            "organizer": event.organizer.name if event.organizer else "Unknown",
            "mode": event.mode,
            "eligibility": event.eligibility,
            "team_size": event.team_size.dict() if event.team_size else {}
        }
        
        prompt = f"""You are a personalized hackathon recommendation assistant. Analyze the event and user profile, then generate a personalized JSON response.

**EVENT DATA:**
{json.dumps(event_summary, indent=2)}

**USER PROFILE:**
- Skills: {user_skills}
- Interests: {user_interests}
- Experience Level: {user_experience}
- Past Events: {len(user_profile.events_attended)}
- Projects: {len(user_profile.projects)}

**TASK:** Generate ONLY a valid JSON object (no markdown, no explanations) with these exact fields:

{{
  "personalized_description": "A 150-word engaging description tailored to this user's skills and interests",
  "why_you_should_participate": "A 100-word explanation of why this user should join",
  "skills_you_will_learn": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "skills_required": [{{"skill": "Python", "user_has": true}}, {{"skill": "React", "user_has": false}}],
  "match_score": 85,
  "personalized_tips": ["tip1", "tip2", "tip3"],
  "challenge_level": "perfect-fit",
  "networking_opportunities": "Brief description of networking value"
}}

Return ONLY the JSON object above. No other text."""
        
        return prompt
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's JSON response"""
        
        try:
            # Remove markdown code blocks if present
            cleaned = response_text.strip()
            
            # Remove ```json and ``` markers
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            logger.info(f"[Personalization] Cleaned response: {cleaned[:200]}...")
            
            # Parse JSON
            parsed = json.loads(cleaned)
            
            logger.info(f"[Personalization] ✅ Successfully parsed JSON")
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error(f"[Personalization] ❌ JSON parse error: {e}")
            logger.error(f"[Personalization] Response text: {response_text[:500]}")
            
            return {
                "personalized_description": "Unable to generate personalized description",
                "why_you_should_participate": "This event matches your profile",
                "skills_you_will_learn": ["Problem solving", "Team collaboration"],
                "skills_required": [],
                "match_score": 50,
                "personalized_tips": ["Prepare well", "Network actively"],
                "challenge_level": "moderate",
                "networking_opportunities": "Meet like-minded participants",
                "error": str(e)
            }


personalization_service = PersonalizationService()
