import asyncio
from app.config.firebase_config import initialize_firebase
from app.queue.queue_manager import queue_manager
from app.queue.processor import queue_processor

async def quick_populate():
    # Initialize Firebase
    initialize_firebase()
    print("✅ Firebase initialized")
    
    # Add sample URLs
    test_urls = [
        "https://unstop.com/competitions/cosmoquest-advitiya26-indian-institute-of-technology-iit-ropar-1618073",
        "https://unstop.com/competitions/the-great-literary-auction-infusion-2026-iim-rohtak-1616755"
    ]
    
    print("\n📥 Adding URLs to queue...")
    for url in test_urls:
        queue_id = await queue_manager.add_to_queue(url, "Unstop", priority=10)
        print(f"  ✅ Added: {queue_id}")
    
    print("\n⚙️ Processing queue (this may take 1-2 minutes)...")
    await queue_processor.process_queue(max_concurrent=2)
    
    print("\n✅ Done! Run get_event_id.py to see events.")

if __name__ == "__main__":
    asyncio.run(quick_populate())
