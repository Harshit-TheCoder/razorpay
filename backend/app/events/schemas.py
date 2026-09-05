from pydantic import BaseModel, Field
from typing import Any, Dict
from datetime import datetime

class BaseEvent(BaseModel):
    event_type: str
    merchant_id: str
    source: str
    external_event_id: str
    payload: Dict[str, Any]
    processed_at: datetime = Field(default_factory=datetime.utcnow)

class PaymentFailedEvent(BaseEvent):
    event_type: str = "payment.failed"
    source: str = "razorpay"
