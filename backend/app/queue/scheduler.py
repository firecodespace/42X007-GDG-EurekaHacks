import asyncio
from datetime import datetime, timedelta
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from app.queue.queue_manager import queue_manager
from app.queue.processor import queue_processor
from app.discovery.unstop_indexer import UnstopIndexer
from app.shared.logger import logger


class AutomatedScheduler:
    """Automated scheduler for discovery and extraction"""
    
    def __init__(self):
        self.scheduler = None
        self.is_running = False
        self.indexers = {
            "unstop": UnstopIndexer()
        }
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            logger.warning("[Scheduler] Already running")
            return
        
        # Initialize scheduler with event loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        
        self.scheduler = AsyncIOScheduler(event_loop=loop)
        
        # Add event listeners
        self.scheduler.add_listener(self._job_executed, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(self._job_error, EVENT_JOB_ERROR)
        
        # Job 1: Process queue every 10 minutes
        self.scheduler.add_job(
            self._process_queue_job,
            trigger=IntervalTrigger(minutes=10),
            id="process_queue",
            name="Process Extraction Queue",
            replace_existing=True
        )
        
        # Job 2: Discover Unstop URLs every 6 hours
        self.scheduler.add_job(
            self._discover_unstop_job,
            trigger=IntervalTrigger(hours=6),
            id="discover_unstop",
            name="Discover Unstop Events",
            replace_existing=True
        )
        
        # Job 3: Daily cleanup at 2 AM
        self.scheduler.add_job(
            self._cleanup_job,
            trigger=CronTrigger(hour=2, minute=0),
            id="cleanup",
            name="Daily Cleanup",
            replace_existing=True
        )
        
        # Job 4: Daily stats report at 9 AM
        self.scheduler.add_job(
            self._stats_report_job,
            trigger=CronTrigger(hour=9, minute=0),
            id="stats_report",
            name="Daily Stats Report",
            replace_existing=True
        )
        
        self.scheduler.start()
        self.is_running = True
        logger.info("[Scheduler] ✅ Started successfully")
        logger.info("[Scheduler] Jobs scheduled:")
        for job in self.scheduler.get_jobs():
            logger.info(f"  - {job.name} (ID: {job.id})")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            return
        
        if self.scheduler:
            self.scheduler.shutdown()
        self.is_running = False
        logger.info("[Scheduler] Stopped")
    
    def _job_executed(self, event):
        """Callback when job executes successfully"""
        logger.info(f"[Scheduler] ✅ Job executed: {event.job_id}")
    
    def _job_error(self, event):
        """Callback when job fails"""
        logger.error(f"[Scheduler] ❌ Job failed: {event.job_id} - {event.exception}")
    
    async def _process_queue_job(self):
        """Job: Process extraction queue"""
        try:
            logger.info("[Scheduler] 🔄 Running: Process Queue")
            await queue_processor.process_queue(max_concurrent=3)
            logger.info("[Scheduler] ✅ Process Queue completed")
        except Exception as e:
            logger.error(f"[Scheduler] Process queue job failed: {e}")
    
    async def _discover_unstop_job(self):
        """Job: Discover new Unstop events"""
        try:
            logger.info("[Scheduler] 🔍 Running: Discover Unstop")
            
            indexer = self.indexers["unstop"]
            
            # Discover URLs
            result = await indexer.discover_with_metadata(max_pages=3)
            urls = result.get("urls", [])
            
            logger.info(f"[Scheduler] Discovered {len(urls)} URLs from Unstop")
            
            # Add to queue
            added_count = 0
            for url in urls:
                queue_id = await queue_manager.add_to_queue(
                    url=url,
                    platform="Unstop",
                    priority=5
                )
                if queue_id:
                    added_count += 1
            
            logger.info(f"[Scheduler] ✅ Added {added_count} new URLs to queue")
            
        except Exception as e:
            logger.error(f"[Scheduler] Discover job failed: {e}")
    
    async def _cleanup_job(self):
        """Job: Clean up old completed/failed items"""
        try:
            logger.info("[Scheduler] 🧹 Running: Cleanup")
            
            from app.config.firebase_config import get_firestore_client
            db = get_firestore_client()
            
            cutoff_date = datetime.utcnow() - timedelta(days=7)
            
            # Delete old completed items
            completed_query = db.collection("extraction_queue")\
                .where("status", "==", "completed")\
                .where("updated_at", "<", cutoff_date)\
                .stream()
            
            deleted_count = 0
            for doc in completed_query:
                doc.reference.delete()
                deleted_count += 1
            
            logger.info(f"[Scheduler] Cleaned up {deleted_count} old queue items")
            
            # Reset failed items
            failed_query = db.collection("extraction_queue")\
                .where("status", "==", "failed")\
                .where("attempts", ">=", 3)\
                .stream()
            
            reset_count = 0
            for doc in failed_query:
                doc.reference.delete()
                reset_count += 1
            
            logger.info(f"[Scheduler] ✅ Removed {reset_count} permanently failed items")
            
        except Exception as e:
            logger.error(f"[Scheduler] Cleanup job failed: {e}")
    
    async def _stats_report_job(self):
        """Job: Generate daily stats report"""
        try:
            logger.info("[Scheduler] 📊 Running: Stats Report")
            
            stats = await queue_manager.get_queue_stats()
            
            from app.persistence.firestore_repo import firestore_repo
            events = await firestore_repo.list_events(limit=1000)
            
            logger.info("=" * 50)
            logger.info("📊 DAILY STATS REPORT")
            logger.info("=" * 50)
            logger.info(f"Queue Status:")
            logger.info(f"  - Pending: {stats.get('pending', 0)}")
            logger.info(f"  - Processing: {stats.get('processing', 0)}")
            logger.info(f"  - Completed: {stats.get('completed', 0)}")
            logger.info(f"  - Failed: {stats.get('failed', 0)}")
            logger.info(f"\nTotal Events in Database: {len(events)}")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"[Scheduler] Stats report job failed: {e}")
    
    def run_job_now(self, job_id: str):
        """Manually trigger a job"""
        try:
            job = self.scheduler.get_job(job_id)
            if job:
                job.modify(next_run_time=datetime.now())
                logger.info(f"[Scheduler] Triggered job: {job_id}")
            else:
                logger.error(f"[Scheduler] Job not found: {job_id}")
        except Exception as e:
            logger.error(f"[Scheduler] Failed to trigger job: {e}")


automated_scheduler = AutomatedScheduler()
