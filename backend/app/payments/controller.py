from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db_session
from app.payments.repository import PaymentRepository
from app.payments.service import PaymentService
from app.payments.schemas import PaymentCreateDTO, PaymentResponseDTO
from typing import List

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_payment_service(session: AsyncSession = Depends(get_db_session)) -> PaymentService:
    repo = PaymentRepository(session)
    return PaymentService(repo)

@router.post("/", response_model=PaymentResponseDTO)
async def create_payment(
    data: PaymentCreateDTO,
    service: PaymentService = Depends(get_payment_service)
):
    return await service.create_payment(data)

@router.get("", response_model=List[PaymentResponseDTO])
async def list_payments(
    service: PaymentService = Depends(get_payment_service)
):
    return await service.list_payments()

@router.get("/{payment_id}", response_model=PaymentResponseDTO)
async def get_payment(
    payment_id: str,
    service: PaymentService = Depends(get_payment_service)
):
    return await service.get_payment(payment_id)
