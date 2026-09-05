from pydantic import BaseModel
from typing import Dict, Any, Optional

class NotificationPayload(BaseModel):
    customer_id: str
    template_id: str
    context_data: Dict[str, Any]
    channel: str = "email" # 'email' or 'sms'

class NotificationResult(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
