from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.db.session import get_db_session
from app.policies.models import PolicyProfile
from app.policies.schemas import PolicyProfileDTO, PolicyProfileResponseDTO

router = APIRouter(prefix="/merchants/{merchant_id}/policies", tags=["Policies"])

@router.get("", response_model=PolicyProfileResponseDTO)
async def get_policy(merchant_id: str, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(
        select(PolicyProfile).where(PolicyProfile.merchant_id == merchant_id)
    )
    policy = result.scalars().first()
    
    if not policy:
        # Create default policy if none exists
        policy = PolicyProfile(merchant_id=merchant_id)
        session.add(policy)
        await session.commit()
        await session.refresh(policy)
        
    return PolicyProfileResponseDTO(**policy.__dict__)

@router.put("", response_model=PolicyProfileResponseDTO)
async def update_policy(merchant_id: str, data: PolicyProfileDTO, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(
        select(PolicyProfile).where(PolicyProfile.merchant_id == merchant_id)
    )
    policy = result.scalars().first()
    
    if not policy:
        policy = PolicyProfile(merchant_id=merchant_id)
        session.add(policy)
        
    policy.max_retries = data.max_retries
    policy.max_transaction_amount = data.max_transaction_amount
    policy.max_contacts = data.max_contacts
    policy.recovery_window_days = data.recovery_window_days
    policy.require_human_approval = data.require_human_approval
    
    await session.commit()
    await session.refresh(policy)
    
    return PolicyProfileResponseDTO(**policy.__dict__)
