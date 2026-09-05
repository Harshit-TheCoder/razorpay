from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.db.session import get_db_session
from app.recovery.models import RecoveryCase
from app.recovery.schemas import RecoveryCaseResponseDTO

router = APIRouter(prefix="/escalations", tags=["Escalations"])

@router.get("", response_model=List[RecoveryCaseResponseDTO])
async def list_escalations(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(
        select(RecoveryCase).where(RecoveryCase.state == "ESCALATED").order_by(RecoveryCase.opened_at.desc())
    )
    cases = result.scalars().all()
    return [RecoveryCaseResponseDTO(**c.__dict__) for c in cases]

@router.post("/{case_id}/resolve")
async def resolve_escalation(case_id: str, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(
        select(RecoveryCase).where(RecoveryCase.id == case_id)
    )
    case = result.scalars().first()
    
    from datetime import datetime
    
    if not case:
        return {"error": "Case not found"}
        
    case.state = "CLOSED" # Resolving moves it directly to CLOSED so it counts as recovered.
    case.closed_at = datetime.utcnow()
    await session.commit()
    
    return {"status": "success", "case_id": case_id, "new_state": case.state}
