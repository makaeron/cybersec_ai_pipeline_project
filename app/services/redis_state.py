import time  # Use time to create rolling windows.  

import redis  # Redis Python client.  

from app.config import settings  # Read app settings.  


class RedisState:  # Helper methods for dedupe and rate limiting.  
    def __init__(self) -> None:  # Build the Redis client.  
        self.client = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)  # Connect to Redis.  

    def seen_event(self, event_id: str) -> bool:  # Check whether an event was already processed.  
        key = f"event:{event_id}"  # Build a unique Redis key.  
        if self.client.exists(key):  # If key already exists, the event was seen before.  
            return True  # Return true for duplicate.  
        self.client.set(key, "1", ex=600)  # Save the key for 10 minutes.  
        return False  # Return false for new event.  

    def allow_llm_call(self) -> bool:  # Limit how often the LLM can be called.  
        minute_key = f"llm:{int(time.time() // 60)}"  # Create one key per minute.  
        current_count = self.client.incr(minute_key)  # Increase the counter for the current minute.  
        self.client.expire(minute_key, 70)  # Auto-delete shortly after the minute ends.  
        return current_count <= settings.llm_rate_limit_per_minute  # Allow only up to the configured limit.
