from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .token_bucket import consume_token, RateLimitExceededError

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow health checks and internal paths to bypass
        if request.url.path.startswith("/health") or request.url.path.startswith("/internal"):
            return await call_next(request)
            
        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:ip:{client_ip}"
        
        try:
            # Default rate limit: 50 requests per second burst, 10 per sec average
            await consume_token(key, capacity=50, refill_rate_per_sec=10.0)
        except RateLimitExceededError as e:
            return JSONResponse(
                status_code=429,
                content={"error_code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests"},
                headers={"Retry-After": str(e.retry_after)}
            )
            
        response = await call_next(request)
        return response
