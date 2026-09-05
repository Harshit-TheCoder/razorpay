from pydantic import BaseModel
from typing import Optional

class PaymentCreateDTO(BaseModel):
    merchant_id: str
    order_id: Optional[str] = None
    razorpay_payment_id: str
    status: str
    error_code: Optional[str] = None
    error_reason: Optional[str] = None
    error_source: Optional[str] = None

class PaymentResponseDTO(PaymentCreateDTO):
    id: str

class OrderCreateDTO(BaseModel):
    merchant_id: str
    customer_id: str
    razorpay_order_id: str
    status: str

class OrderResponseDTO(OrderCreateDTO):
    id: str
