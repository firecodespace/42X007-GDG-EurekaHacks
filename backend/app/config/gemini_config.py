import google.generativeai as genai
from app.config.settings import settings
from app.shared.logger import logger


_gemini_model = None


def initialize_gemini() -> None:
    """Initialize Gemini API"""
    try:
        genai.configure(api_key=settings.gemini_api_key)
        logger.info("Gemini API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Gemini: {e}")
        raise


def get_gemini_model(model_name: str = "gemini-1.5-flash"):
    """Get Gemini model instance"""
    global _gemini_model
    
    if _gemini_model is None:
        try:
            _gemini_model = genai.GenerativeModel(model_name)
            logger.info(f"Gemini model '{model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Gemini model: {e}")
            raise
    
    return _gemini_model
