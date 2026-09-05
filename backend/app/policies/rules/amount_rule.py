from .base import BaseRule
from app.recovery.schemas import ActionProposal

class AmountRule(BaseRule):
    """
    Prevents offering a discount if the cart value is too low.
    """
    
    @property
    def rule_name(self) -> str:
        return "minimum_amount_for_discount_rule"
        
    async def evaluate(self, merchant_id: str, action: ActionProposal) -> bool:
        if action.action_type != "offer_discount":
            return True
            
        amount = action.payload.get("original_amount", 0)
        # Prevent discounts on tiny orders
        if amount < 500: # Example: less than 500 INR
            return False
            
        return True
