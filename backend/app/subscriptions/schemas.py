
from pydantic import BaseModel
from typing import Optional

class SubscriptionCreateDTO(BaseModel):
    merchant_id: str
    customer_id: str
    razorpay_subscription_id: Optional[str] = None
    plan_id: Optional[str] = None
    next_billing_at: Optional[str] = None
    failure_count: int = 0
    type: Optional[str] = None
    status: str

class SubscriptionResponseDTO(SubscriptionCreateDTO):
    id: str

class SubscriptionChargeCreateDTO(BaseModel):
    subscription_id: str
    razorpay_invoice_id: Optional[str] = None
    status: str
    attempt_number: int = 1

class SubscriptionChargeResponseDTO(SubscriptionChargeCreateDTO):
    id: str
