from typing import Dict, Any
from app.agent.strategies.base import RecoveryStrategy

class CheckoutAbandonmentStrategy(RecoveryStrategy):
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["enriched_data"] = {
            "cart_value": context.get("cart_value", 0),
            "customer_history": "new_user",
            "abandonment_time_mins": 45
        }
        return context

    def get_system_prompt(self) -> str:
        return """You are evaluating CHECKOUT ABANDONMENT.
Consider the cart value and customer history to determine the best intervention.
Allowed actions:
- 'send_reminder': If it's a new user and a small cart value.
- 'offer_discount': If the cart value is high to prevent loss of a big sale.
- 'escalate': Unlikely for abandonment, but possible.
Output the exact JSON matching the schema."""
