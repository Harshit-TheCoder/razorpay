from pydantic import BaseModel
from typing import Optional, Dict, Any

class CheckoutCreateDTO(BaseModel):
    merchant_id: str
    customer_id: str
    order_id: Optional[str] = None
    cart_snapshot: Optional[Dict[str, Any]] = None
    status: str

class CheckoutResponseDTO(CheckoutCreateDTO):
    id: str
