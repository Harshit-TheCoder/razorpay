from fastapi import APIRouter
from app.payments.controller import router as payments_router
from app.checkout.controller import router as checkout_router
from app.subscriptions.controller import router as subscriptions_router
from app.recovery.controller import router as recovery_router
from app.analytics.controller import router as analytics_router
from app.api.v1.escalations import router as escalations_router
from app.policies.controller import router as policies_router
from app.api.v1.audit import router as audit_router
from app.api.v1.live import router as live_router

api_router = APIRouter()

api_router.include_router(payments_router)
api_router.include_router(checkout_router)
api_router.include_router(subscriptions_router)
api_router.include_router(recovery_router)
api_router.include_router(analytics_router)
api_router.include_router(escalations_router)
api_router.include_router(policies_router)
api_router.include_router(audit_router)
api_router.include_router(live_router)

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}
