from typing import Dict, Any
from app.agent.strategies.base import RecoveryStrategy

class ChurnRecoveryStrategy(RecoveryStrategy):
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["enriched_data"] = {
            "churn_risk": "high",
            "last_active_days_ago": 14,
            "lifetime_value": 5000
        }
        return context

    def get_system_prompt(self) -> str:
        return """You are evaluating a CUSTOMER CHURN risk.
Analyze the customer's lifetime value and inactivity.
Allowed actions:
- 'send_discount': To incentivize a high-LTV customer to return.
- 'send_reminder': A gentle nudge for a medium-LTV customer.
- 'ignore': If LTV is too low to warrant an intervention.
Output the exact JSON matching the schema."""
