import requests

print("🔍 Triggering Unstop discovery...")
response = requests.post("http://localhost:8000/api/v1/queue/scheduler/trigger/discover_unstop")
print(response.json())

print("\n📊 Checking queue stats...")
response = requests.get("http://localhost:8000/api/v1/queue/stats")
print(response.json())
