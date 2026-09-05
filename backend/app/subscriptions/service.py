from app.subscriptions.repository import SubscriptionRepository
from app.subscriptions.schemas import SubscriptionCreateDTO, SubscriptionResponseDTO
from app.subscriptions.models import Subscription
from app.exceptions.domain_exceptions import SubscriptionNotFoundError

class SubscriptionService:
    def __init__(self, repository: SubscriptionRepository):
        self.repository = repository
        
    async def create_subscription(self, data: SubscriptionCreateDTO) -> SubscriptionResponseDTO:
        obj = Subscription(**data.model_dump())
        created = await self.repository.create(obj)
        return SubscriptionResponseDTO(**created.__dict__)
        
    async def get_subscription(self, sub_id: str) -> SubscriptionResponseDTO:
        sub = await self.repository.get(sub_id)
        if not sub:
            raise SubscriptionNotFoundError(subscription_id=sub_id)
        return SubscriptionResponseDTO(**sub.__dict__)

    async def list_subscriptions(self, limit: int = 20) -> list[SubscriptionResponseDTO]:
        subs = await self.repository.list(limit=limit)
        return [SubscriptionResponseDTO(**sub.__dict__) for sub in subs]
