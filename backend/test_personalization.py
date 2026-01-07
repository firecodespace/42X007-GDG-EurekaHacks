import requests
import json

# Sample user profile
user_profile = {
    "user_id": "user123",
    "skills": ["Python", "React", "Machine Learning", "Docker"],
    "interests": ["AI/ML", "Web Development", "Cloud Computing"],
    "experience_level": "intermediate",
    "events_attended": [
        {"event_id": "e1", "name": "MLH Hackathon 2024"}
    ],
    "projects": [
        {"name": "AI Chatbot", "tech": ["Python", "OpenAI"]}
    ]
}

# Get an event ID from your Firestore
event_id = "79d48242750f7ffb"  # Replace with actual ID

# Call personalization API
response = requests.post(
    f"http://localhost:8000/api/v1/personalization/personalize/{event_id}",
    json=user_profile
)

# Print result
result = response.json()
print(json.dumps(result, indent=2))
