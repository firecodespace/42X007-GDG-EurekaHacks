import asyncio
from app.config.firebase_config import initialize_firebase
from app.persistence.firestore_repo import firestore_repo

async def get_event():
    # Initialize Firebase
    initialize_firebase()
    print("✅ Firebase initialized")
    
    # Get events
    events = await firestore_repo.list_events(limit=5)
    
    if events:
        print(f"\n📋 Found {len(events)} events in Firestore:\n")
        for i, event in enumerate(events, 1):
            print(f"{i}. Event ID: {event.id}")
            print(f"   Title: {event.title}")
            
            # Print available fields
            event_dict = event.model_dump()
            if 'source_platform' in event_dict:
                print(f"   Platform: {event_dict['source_platform']}")
            if 'organizer' in event_dict:
                print(f"   Organizer: {event_dict['organizer']}")
            if 'event_mode' in event_dict:
                print(f"   Mode: {event_dict['event_mode']}")
            
            print()
        
        print(f"✅ Use this Event ID for testing: {events[0].id}")
        return events[0].id
    else:
        print("❌ No events in Firestore!")
        print("\n💡 Run quick_populate.py to add test events")
        return None

if __name__ == "__main__":
    event_id = asyncio.run(get_event())
