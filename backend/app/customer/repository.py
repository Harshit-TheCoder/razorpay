from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.core.db.postgres.base_models import Customer
from app.payments.models import Payment, Order
from app.subscriptions.models import Subscription

class CustomerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_customer(self, customer_id: str) -> Optional[Customer]:
        result = await self.session.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalars().first()

    async def count_customer_orders(self, customer_id: str) -> int:
        result = await self.session.execute(select(func.count(Order.id)).where(Order.customer_id == customer_id))
        return result.scalar() or 0

    async def get_customer_payment_stats(self, customer_id: str) -> dict:
        # Simplistic approach for skeleton
        result = await self.session.execute(
            select(Payment.status, func.count(Payment.id))
            .join(Order, Payment.order_id == Order.id)
            .where(Order.customer_id == customer_id)
            .group_by(Payment.status)
        )
        stats = {"total": 0, "successful": 0, "failed": 0}
        for status, count in result.all():
            stats["total"] += count
            if status == "captured":
                stats["successful"] += count
            elif status == "failed":
                stats["failed"] += count
        return stats
