import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Checking configuration...")
print()

# Check .env
gemini_key = os.getenv("GEMINI_API_KEY")
firebase_project = os.getenv("FIREBASE_PROJECT_ID")
creds_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

print(f"✅ GEMINI_API_KEY: {'Set' if gemini_key and gemini_key != 'your_actual_gemini_api_key_here' else '❌ NOT SET'}")
print(f"✅ FIREBASE_PROJECT_ID: {firebase_project if firebase_project and firebase_project != 'your_firebase_project_id' else '❌ NOT SET'}")
print()

# Check gcp-sa.json
if os.path.exists(creds_path):
    print(f"✅ Firebase credentials file found: {creds_path}")
else:
    print(f"❌ Firebase credentials file NOT found: {creds_path}")
print()

print("Configuration check complete!")
