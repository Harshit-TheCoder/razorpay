from app.checkout.repository import CheckoutRepository
from app.checkout.schemas import CheckoutCreateDTO, CheckoutResponseDTO
from app.checkout.models import CheckoutRecord

class CheckoutService:
    def __init__(self, repository: CheckoutRepository):
        self.repository = repository
        
    async def log_checkout(self, data: CheckoutCreateDTO) -> CheckoutResponseDTO:
        obj = CheckoutRecord(**data.model_dump())
        created = await self.repository.create(obj)
        return CheckoutResponseDTO(**created.__dict__)

    async def list_checkouts(self, limit: int = 20) -> list[CheckoutResponseDTO]:
        checkouts = await self.repository.list(limit=limit)
        return [CheckoutResponseDTO(**checkout.__dict__) for checkout in checkouts]
