from pydantic import BaseModel
from typing import List, Optional

class CustomerHistoryDTO(BaseModel):
    customer_id: str
    total_orders: int
    total_payments: int
    successful_payments: int
    failed_payments: int
    active_subscriptions: int
    
class CustomerProfileDTO(BaseModel):
    customer_id: str
    merchant_id: str
    history: CustomerHistoryDTO
