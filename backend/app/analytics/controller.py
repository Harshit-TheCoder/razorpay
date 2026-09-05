from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db_session
from app.analytics.service import AnalyticsService
from app.analytics.schemas import RecoveryMetricsDTO

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_analytics_service(session: AsyncSession = Depends(get_db_session)) -> AnalyticsService:
    return AnalyticsService(session)

@router.get("/metrics/{merchant_id}", response_model=RecoveryMetricsDTO)
async def get_metrics(merchant_id: str, service: AnalyticsService = Depends(get_analytics_service)):
    return await service.get_recovery_metrics(merchant_id)
