from pydantic import BaseModel
from typing import Optional

class SubscriptionCreateDTO(BaseModel):
    merchant_id: str
    customer_id: str
    razorpay_subscription_id: str
    type: str
    status: str

class SubscriptionResponseDTO(SubscriptionCreateDTO):
    id: str

class SubscriptionChargeCreateDTO(BaseModel):
    subscription_id: str
    razorpay_invoice_id: str
    status: str
    attempt_number: int = 1

class SubscriptionChargeResponseDTO(SubscriptionChargeCreateDTO):
    id: str
