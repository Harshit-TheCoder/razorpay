from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db_session
from app.checkout.repository import CheckoutRepository
from app.checkout.service import CheckoutService
from app.checkout.schemas import CheckoutCreateDTO, CheckoutResponseDTO
from typing import List

router = APIRouter(prefix="/checkout", tags=["Checkout"])

def get_checkout_service(session: AsyncSession = Depends(get_db_session)) -> CheckoutService:
    repo = CheckoutRepository(session)
    return CheckoutService(repo)

@router.post("/", response_model=CheckoutResponseDTO)
async def log_checkout(
    data: CheckoutCreateDTO,
    service: CheckoutService = Depends(get_checkout_service)
):
    return await service.log_checkout(data)

@router.get("", response_model=List[CheckoutResponseDTO])
async def list_checkouts(
    service: CheckoutService = Depends(get_checkout_service)
):
    return await service.list_checkouts()
