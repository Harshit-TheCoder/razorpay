from pydantic import BaseModel
from typing import Optional

class PolicyProfileDTO(BaseModel):
    merchant_id: str
    max_retries: int = 2
    max_transaction_amount: int = 10000
    max_contacts: int = 3
    recovery_window_days: int = 7
    require_human_approval: bool = False

class PolicyProfileResponseDTO(PolicyProfileDTO):
    id: str
