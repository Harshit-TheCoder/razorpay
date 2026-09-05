from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1.router import api_router
from app.exceptions.base import AppException
from app.exceptions.handlers import app_exception_handler
from app.core.logging import setup_logging
from app.core.rate_limit.middleware import RateLimitMiddleware

settings = get_settings()

def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        debug=settings.DEBUG
    )

    @app.on_event("startup")
    async def startup_event():
        import asyncio
        from app.jobs.anomaly_detector import detect_anomalies_loop
        from app.events.subscribers import setup_subscribers
        from app.recovery.saga import setup_saga_subscribers
        setup_subscribers()
        setup_saga_subscribers()
        asyncio.create_task(detect_anomalies_loop())

    # Register Middlewares
    app.add_middleware(RateLimitMiddleware)

    # Register Exception Handlers
    app.add_exception_handler(AppException, app_exception_handler)

    # Register Routers
    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
