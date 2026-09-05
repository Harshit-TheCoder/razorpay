from typing import Optional
from app.payments.repository import PaymentRepository
from app.payments.schemas import PaymentCreateDTO, PaymentResponseDTO
from app.payments.models import Payment
from app.exceptions.domain_exceptions import PaymentNotFoundError

class PaymentService:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository
        
    async def create_payment(self, data: PaymentCreateDTO) -> PaymentResponseDTO:
        payment_obj = Payment(**data.model_dump())
        created_payment = await self.repository.create(payment_obj)
        return PaymentResponseDTO(**created_payment.__dict__)
        
    async def get_payment(self, payment_id: str) -> PaymentResponseDTO:
        payment = await self.repository.get(payment_id)
        if not payment:
            raise PaymentNotFoundError(payment_id=payment_id)
        return PaymentResponseDTO(**payment.__dict__)

    async def list_payments(self, limit: int = 20) -> list[PaymentResponseDTO]:
        payments = await self.repository.list(limit=limit)
        return [PaymentResponseDTO(**payment.__dict__) for payment in payments]
