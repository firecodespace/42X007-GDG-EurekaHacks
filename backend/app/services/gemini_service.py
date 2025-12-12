import google.generativeai as genai
from app.utils.constants import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)

def analyze_event(event_data):
    prompt = f"""
    Analyze this competition event and extract:
    - Required skills
    - Difficulty level (1-10)
    - Time commitment
    - Ideal team size
    - Event category (AI/Web/Cloud/Startup/etc.)
    - Summary (3 lines)

    Event:
    {event_data}
    """

    model = genai.GenerativeModel("gemini-pro")
    result = model.generate_content(prompt)

    return result.text
