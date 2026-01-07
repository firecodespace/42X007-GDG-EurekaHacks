import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Your user ID (from your profile)
user_id = "2pfMvFhhzsZf7fQpcY4mgTTHhc52"

print("🎯 Testing Final Personalized JSON\n")
print("="*60)

# Step 1: Get your profile to confirm it exists
print("\n1️⃣ Fetching your profile...")
response = requests.get(f"{BASE_URL}/profiles/{user_id}")

if response.status_code == 404:
    print("❌ Profile not found! Creating it first...")
    
    # Create profile
    profile = {
        "user_id": user_id,
        "skills": ["Java", "Python", "Php"],
        "work_experience": [{"years": 3, "role": "Software Engineer", "company": "Microsoft"}],
        "events_attended": [],
        "projects": [],
        "interests": ["AI/ML"],
        "experience_level": "beginner",
        "preferred_domains": ["Dev Ops"],
        "location": "Noida, Uttar Pradesh",
        "university": "Amity University"
    }
    
    response = requests.post(f"{BASE_URL}/profiles/", json=profile)
    print(f"✅ Profile created: {response.json()}")
else:
    print(f"✅ Profile found!")
    profile = response.json()
    print(f"   Skills: {', '.join(profile['skills'][:3])}...")
    print(f"   Experience: {profile['experience_level']}")

# Step 2: Get an event ID
print("\n2️⃣ Fetching available events...")
response = requests.get(f"{BASE_URL}/events/?limit=3")
events = response.json()

if not events:
    print("❌ No events found! Run quick_populate.py first.")
    exit(1)

event_id = events[0]['id']
event_title = events[0]['title']
print(f"✅ Found {len(events)} events")
print(f"   Testing with: {event_title}")

# Step 3: Get personalized JSON (THIS IS THE MAGIC!)
print(f"\n3️⃣ Generating personalized JSON for: {event_title}")
print("   ⏳ This may take 30-60 seconds (first time)...\n")

# Prepare request body (just user_id is enough now)
response = requests.post(
    f"{BASE_URL}/personalization/personalize/{event_id}",
    json=profile,  # Send full profile
    timeout=120
)

if response.status_code == 200:
    result = response.json()
    
    print("="*60)
    print("✅ SUCCESS! Here's your FINAL PERSONALIZED JSON:")
    print("="*60)
    
    # Extract the good stuff
    event_data = result['data']
    personalization = event_data['personalization']
    
    # Display key info
    print(f"\n📋 EVENT: {event_data['title']}")
    print(f"🏛️ Organizer: {event_data['organizer']['name']}")
    print(f"📍 Mode: {event_data['mode']}")
    
    print(f"\n🎯 MATCH SCORE: {personalization['match_score']}/100")
    print(f"🎚️ Challenge Level: {personalization['challenge_level']}")
    
    print(f"\n📝 Personalized Description:")
    print(f"   {personalization['personalized_description'][:200]}...")
    
    print(f"\n💪 Why You Should Participate:")
    print(f"   {personalization['why_you_should_participate'][:200]}...")
    
    print(f"\n📚 Skills You'll Learn:")
    for skill in personalization['skills_you_will_learn']:
        print(f"   • {skill}")
    
    print(f"\n🔧 Skills Required:")
    for skill_obj in personalization['skills_required']:
        status = "✅ You have this" if skill_obj['user_has'] else "❌ Need to learn"
        print(f"   {status}: {skill_obj['skill']}")
    
    print(f"\n💡 Personalized Tips:")
    for i, tip in enumerate(personalization['personalized_tips'], 1):
        print(f"   {i}. {tip}")
    
    print(f"\n🤝 Networking:")
    print(f"   {personalization['networking_opportunities']}")
    
    # Save full JSON
    filename = f"final_personalized_{event_id}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Full JSON saved to: {filename}")
    print("="*60)
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
