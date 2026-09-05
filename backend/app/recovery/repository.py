from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List, Any
from app.core.db.base_repository import AbstractRepository
from app.recovery.models import RecoveryCase, RecoveryAttempt

class RecoveryCaseRepository(AbstractRepository[RecoveryCase]):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get(self, id: Any) -> Optional[RecoveryCase]:
        result = await self.session.execute(select(RecoveryCase).where(RecoveryCase.id == id).with_for_update())
        return result.scalars().first()

    async def list(self, limit: int = 20, cursor: Optional[str] = None, **kwargs) -> List[RecoveryCase]:
        result = await self.session.execute(select(RecoveryCase).limit(limit))
        return list(result.scalars().all())

    async def create(self, obj: RecoveryCase) -> RecoveryCase:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: Any, obj: RecoveryCase) -> RecoveryCase:
        await self.session.merge(obj)
        await self.session.commit()
        return obj

    async def delete(self, id: Any) -> bool:
        return False
