import functools
import json
from typing import Callable, Any
from .redis_client import redis_client

def cached(ttl: int = 300):
    """
    Cache decorator for async functions.
    Requires arguments to be stringifiable.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__module__}.{func.__name__}:{args}:{kwargs}"
            cached_value = await redis_client.get(cache_key)
            if cached_value:
                return json.loads(cached_value)
            
            result = await func(*args, **kwargs)
            # Basic serialization assumption (dicts/lists/primitives)
            await redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
