from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Any
from app.core.db.base_repository import AbstractRepository
from app.payments.models import Payment

class PaymentRepository(AbstractRepository[Payment]):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get(self, id: Any) -> Optional[Payment]:
        result = await self.session.execute(select(Payment).where(Payment.id == id))
        return result.scalars().first()

    async def list(self, limit: int = 20, cursor: Optional[str] = None, **kwargs) -> List[Payment]:
        # Simple limit offset for skeleton
        result = await self.session.execute(select(Payment).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj: Payment) -> Payment:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: Any, obj: Payment) -> Payment:
        # Simplistic implementation for skeleton
        await self.session.merge(obj)
        await self.session.commit()
        return obj

    async def delete(self, id: Any) -> bool:
        # Payments shouldn't be deleted per D.13, returning False
        return False
