from app.core.cache.redis_client import redis_client
import structlog

logger = structlog.get_logger(__name__)

class IdempotencyConflictError(Exception):
    pass

async def acquire_idempotency_key(key: str, expire_seconds: int = 86400) -> bool:
    """
    Attempts to set the idempotency key in Redis.
    Returns True if successful, False if the key already exists (duplicate action).
    """
    try:
        # SET nx=True means "set only if it does not exist". Returns True if set, False if not.
        acquired = await redis_client.set(f"idemp:{key}", "executed", nx=True, ex=expire_seconds)
        return bool(acquired)
    except Exception as e:
        logger.error("redis_idempotency_error", error=str(e), key=key)
        # Fail open or fail closed? We fail open to not block processing on redis failure
        # but in strict financial systems you might fail closed.
        return True
