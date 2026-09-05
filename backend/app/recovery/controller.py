from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.db.session import get_db_session
from app.recovery.repository import RecoveryCaseRepository
from app.recovery.schemas import RecoveryCaseResponseDTO, RecoveryAttemptResponseDTO, ActionProposal
from app.recovery.models import RecoveryAttempt
from app.payments.models import Payment
from app.subscriptions.models import Subscription
from app.checkout.models import CheckoutRecord
from sqlalchemy import select

router = APIRouter(prefix="/cases", tags=["Recovery Cases"])

def get_case_repo(session: AsyncSession = Depends(get_db_session)) -> RecoveryCaseRepository:
    return RecoveryCaseRepository(session)

@router.get("", response_model=List[RecoveryCaseResponseDTO])
async def list_cases(repo: RecoveryCaseRepository = Depends(get_case_repo)):
    cases = await repo.list(limit=20)
    return [RecoveryCaseResponseDTO(**case.__dict__) for case in cases]

@router.get("/{case_id}", response_model=RecoveryCaseResponseDTO)
async def get_case(case_id: str, repo: RecoveryCaseRepository = Depends(get_case_repo)):
    case = await repo.get(case_id)
    return RecoveryCaseResponseDTO(**case.__dict__) if case else None

@router.get("/{case_id}/attempts", response_model=List[RecoveryAttemptResponseDTO])
async def get_attempts(case_id: str, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(
        select(RecoveryAttempt).where(RecoveryAttempt.case_id == case_id).order_by(RecoveryAttempt.attempt_number)
    )
    attempts = result.scalars().all()
    return [RecoveryAttemptResponseDTO(**attempt.__dict__) for attempt in attempts]

@router.get("/{case_id}/source")
async def get_source(case_id: str, repo: RecoveryCaseRepository = Depends(get_case_repo), session: AsyncSession = Depends(get_db_session)):
    case = await repo.get(case_id)
    if not case:
        return {"error": "Case not found"}
        
    if case.scenario_type == "failed_payment":
        res = await session.execute(select(Payment).where(Payment.id == case.source_ref))
        payment = res.scalars().first()
        return {"type": "payment", "data": payment.__dict__ if payment else None}
    elif case.scenario_type == "subscription_recovery":
        res = await session.execute(select(Subscription).where(Subscription.id == case.source_ref))
        sub = res.scalars().first()
        return {"type": "subscription", "data": sub.__dict__ if sub else None}
    elif case.scenario_type == "checkout_abandonment":
        res = await session.execute(select(CheckoutRecord).where(CheckoutRecord.id == case.source_ref))
        checkout = res.scalars().first()
        return {"type": "checkout", "data": checkout.__dict__ if checkout else None}
        
    return {"type": "unknown", "data": None}

@router.get("/{case_id}/decisions", response_model=List[ActionProposal])
async def get_decisions(case_id: str, repo: RecoveryCaseRepository = Depends(get_case_repo)):
    from app.agent.service import AgentService
    
    case = await repo.get(case_id)
    if not case:
        return []
        
    agent = AgentService()
    
    # Run a live evaluation with Gemini for demonstration purposes
    action_proposal = await agent.run(case.scenario_type, {"case_id": case.id, "source_ref": case.source_ref})
    
    return [action_proposal]
