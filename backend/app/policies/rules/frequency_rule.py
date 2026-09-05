from .base import BaseRule
from app.recovery.schemas import ActionProposal

class FrequencyRule(BaseRule):
    """
    Prevents spamming the customer with emails/SMS.
    """
    
    @property
    def rule_name(self) -> str:
        return "frequency_cap_rule"
        
    async def evaluate(self, merchant_id: str, action: ActionProposal) -> bool:
        if action.action_type not in ["send_email", "send_sms"]:
            return True
            
        # Stub logic: Imagine checking Redis here for recent contact counts
        # e.g., await redis_client.get(f"contact:{action.payload.get('customer_id')}")
        # Return False if count > threshold
        return True
