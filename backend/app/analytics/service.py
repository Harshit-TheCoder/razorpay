from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.recovery.models import RecoveryCase
from app.analytics.schemas import RecoveryMetricsDTO

class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_recovery_metrics(self, merchant_id: str) -> RecoveryMetricsDTO:
        # Simplistic implementation for skeleton
        total_cases_result = await self.session.execute(
            select(func.count(RecoveryCase.id), func.sum(RecoveryCase.amount))
            .where(RecoveryCase.merchant_id == merchant_id)
        )
        total_row = total_cases_result.first()
        total = total_row[0] or 0
        total_revenue_paise = total_row[1] or 0
        revenue_at_risk = total_revenue_paise / 100.0 # Convert paise to INR
        
        recovered_cases_result = await self.session.execute(
            select(func.count(RecoveryCase.id), func.sum(RecoveryCase.amount))
            .where(RecoveryCase.merchant_id == merchant_id, RecoveryCase.state.in_(["CLOSED", "RECOVERED"]))
        )
        recovered_row = recovered_cases_result.first()
        recovered = recovered_row[0] or 0
        recovered_revenue_paise = recovered_row[1] or 0
        revenue_recovered = recovered_revenue_paise / 100.0 # Convert paise to INR
        
        unresolved_cases_result = await self.session.execute(
            select(func.count(RecoveryCase.id))
            .where(RecoveryCase.merchant_id == merchant_id, RecoveryCase.state != "CLOSED", RecoveryCase.state != "FAILED", RecoveryCase.state != "RECOVERED")
        )
        unresolved = unresolved_cases_result.scalar() or 0
        
        rate = (recovered / total) if total > 0 else 0.0
        
        return RecoveryMetricsDTO(
            merchant_id=merchant_id,
            total_cases=total,
            unresolved_cases=unresolved,
            recovered_cases=recovered,
            recovery_rate=rate,
            revenue_at_risk=revenue_at_risk,
            revenue_recovered=revenue_recovered
        )
