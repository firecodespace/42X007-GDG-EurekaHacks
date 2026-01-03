import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Available Gemini models:\n")

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")

print("\n" + "="*50)
print("Testing with first available model...\n")

# Try to use the first available model
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say hello")
    print(f"✅ SUCCESS with gemini-1.5-flash")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ gemini-1.5-flash failed: {e}")
    
    # Try alternative
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content("Say hello")
        print(f"✅ SUCCESS with models/gemini-1.5-flash")
        print(f"Response: {response.text}")
    except Exception as e2:
        print(f"❌ models/gemini-1.5-flash failed: {e2}")
