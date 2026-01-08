import asyncio
from app.config.firebase_config import initialize_firebase
from app.discovery.unstop_indexer import UnstopIndexer
from app.queue.queue_manager import queue_manager
from app.queue.processor import queue_processor
from app.persistence.firestore_repo import firestore_repo

async def test_layer1():
    # Initialize Firebase using YOUR config
    initialize_firebase()
    
    print("🧪 Testing Layer 1: Discovery & Extraction\n")
    print("="*60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Unstop Connection...")
    indexer = UnstopIndexer()
    health = await indexer.health_check()
    print(f"   {'✅' if health else '❌'} Unstop accessible: {health}")
    
    # Test 2: Discover URLs
    print("\n2️⃣ Discovering URLs from Unstop...")
    result = await indexer.discover_with_metadata(max_pages=1)
    urls = result.get("urls", [])
    print(f"   ✅ Found {len(urls)} URLs")
    if urls:
        print(f"   Sample URLs:")
        for url in urls[:3]:
            print(f"     - {url}")
    
    # Test 3: Queue Status
    print("\n3️⃣ Checking Queue Status...")
    stats = await queue_manager.get_queue_stats()
    print(f"   Pending: {stats.get('pending', 0)}")
    print(f"   Processing: {stats.get('processing', 0)}")
    print(f"   Completed: {stats.get('completed', 0)}")
    print(f"   Failed: {stats.get('failed', 0)}")
    
    # Test 4: Add URLs to Queue
    if urls:
        print(f"\n4️⃣ Adding {min(3, len(urls))} URLs to queue...")
        added = 0
        for url in urls[:3]:
            queue_id = await queue_manager.add_to_queue(url, "Unstop", priority=10)
            if queue_id:
                added += 1
        print(f"   ✅ Added {added} URLs to queue")
    
    # Test 5: Process Queue
    print("\n5️⃣ Processing Queue (1 item)...")
    await queue_processor.process_queue(max_concurrent=1)
    
    # Test 6: Check Events in Database
    print("\n6️⃣ Checking Events in Firestore...")
    events = await firestore_repo.list_events(limit=10)
    print(f"   ✅ Total events in database: {len(events)}")
    if events:
        print(f"   Latest event: {events[0].title}")
        print(f"   Created: {events[0].created_at}")
    
    print("\n" + "="*60)
    print("✅ Layer 1 Test Complete!\n")

if __name__ == "__main__":
    asyncio.run(test_layer1())
