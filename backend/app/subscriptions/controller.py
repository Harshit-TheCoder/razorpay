from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db_session
from app.subscriptions.repository import SubscriptionRepository
from app.subscriptions.service import SubscriptionService
from app.subscriptions.schemas import SubscriptionCreateDTO, SubscriptionResponseDTO
from typing import List

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

def get_subscription_service(session: AsyncSession = Depends(get_db_session)) -> SubscriptionService:
    repo = SubscriptionRepository(session)
    return SubscriptionService(repo)

@router.post("/", response_model=SubscriptionResponseDTO)
async def create_subscription(
    data: SubscriptionCreateDTO,
    service: SubscriptionService = Depends(get_subscription_service)
):
    return await service.create_subscription(data)

@router.get("", response_model=List[SubscriptionResponseDTO])
async def list_subscriptions(
    service: SubscriptionService = Depends(get_subscription_service)
):
    return await service.list_subscriptions()

@router.get("/{sub_id}", response_model=SubscriptionResponseDTO)
async def get_subscription(
    sub_id: str,
    service: SubscriptionService = Depends(get_subscription_service)
):
    return await service.get_subscription(sub_id)
