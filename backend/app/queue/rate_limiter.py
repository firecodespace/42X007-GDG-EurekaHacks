from datetime import datetime, timedelta
from typing import Optional
from app.shared.logger import logger


class RateLimiter:
    """Rate limiter for extraction requests"""
    
    def __init__(
        self, 
        max_per_hour: int = 50,
        max_per_day: int = 500
    ):
        self.max_per_hour = max_per_hour
        self.max_per_day = max_per_day
        self.hourly_count = 0
        self.daily_count = 0
        self.hour_start = datetime.utcnow()
        self.day_start = datetime.utcnow()
    
    def can_proceed(self) -> bool:
        """Check if we can process another request"""
        self._reset_counters()
        
        if self.hourly_count >= self.max_per_hour:
            logger.warning(f"[RateLimiter] Hourly limit reached: {self.hourly_count}/{self.max_per_hour}")
            return False
        
        if self.daily_count >= self.max_per_day:
            logger.warning(f"[RateLimiter] Daily limit reached: {self.daily_count}/{self.max_per_day}")
            return False
        
        return True
    
    def increment(self):
        """Increment counters"""
        self.hourly_count += 1
        self.daily_count += 1
        logger.info(f"[RateLimiter] Count: {self.hourly_count}/{self.max_per_hour} hourly, {self.daily_count}/{self.max_per_day} daily")
    
    def _reset_counters(self):
        """Reset counters if time window passed"""
        now = datetime.utcnow()
        
        # Reset hourly counter
        if now - self.hour_start >= timedelta(hours=1):
            self.hourly_count = 0
            self.hour_start = now
            logger.info("[RateLimiter] Hourly counter reset")
        
        # Reset daily counter
        if now - self.day_start >= timedelta(days=1):
            self.daily_count = 0
            self.day_start = now
            logger.info("[RateLimiter] Daily counter reset")
    
    def get_wait_time(self) -> Optional[int]:
        """Get seconds to wait before next request"""
        self._reset_counters()
        
        if self.hourly_count >= self.max_per_hour:
            wait_seconds = int((self.hour_start + timedelta(hours=1) - datetime.utcnow()).total_seconds())
            return max(wait_seconds, 0)
        
        return 0


rate_limiter = RateLimiter(
    max_per_hour=50,   # Adjust based on your limits
    max_per_day=500
)
