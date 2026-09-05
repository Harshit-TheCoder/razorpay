import time
from app.core.cache.redis_client import redis_client

class RateLimitExceededError(Exception):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after

async def consume_token(key: str, capacity: int = 100, refill_rate_per_sec: float = 1.0) -> bool:
    """
    Token bucket algorithm using Redis.
    Raises RateLimitExceededError if no tokens are available.
    """
    now = time.time()
    
    # Run in a transaction (pipeline)
    async with redis_client.pipeline(transaction=True) as pipe:
        while True:
            try:
                await pipe.watch(key)
                data = await pipe.get(key)
                
                if data:
                    tokens, last_refill = map(float, data.split(':'))
                else:
                    tokens, last_refill = capacity, now
                
                # Refill
                time_passed = now - last_refill
                new_tokens = min(capacity, tokens + time_passed * refill_rate_per_sec)
                
                if new_tokens < 1:
                    # Calculate wait time
                    retry_after = int((1 - new_tokens) / refill_rate_per_sec) + 1
                    await pipe.unwatch()
                    raise RateLimitExceededError(retry_after=retry_after)
                
                pipe.multi()
                pipe.set(key, f"{new_tokens - 1}:{now}", ex=int(capacity / refill_rate_per_sec) + 10)
                await pipe.execute()
                return True
            except Exception as e:
                if isinstance(e, RateLimitExceededError):
                    raise
                # Optimistic locking failed, retry
                continue
