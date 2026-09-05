from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Any
from app.core.db.base_repository import AbstractRepository
from app.subscriptions.models import Subscription

class SubscriptionRepository(AbstractRepository[Subscription]):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get(self, id: Any) -> Optional[Subscription]:
        result = await self.session.execute(select(Subscription).where(Subscription.id == id))
        return result.scalars().first()

    async def list(self, limit: int = 20, cursor: Optional[str] = None, **kwargs) -> List[Subscription]:
        result = await self.session.execute(select(Subscription).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj: Subscription) -> Subscription:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: Any, obj: Subscription) -> Subscription:
        await self.session.merge(obj)
        await self.session.commit()
        return obj

    async def delete(self, id: Any) -> bool:
        return False
