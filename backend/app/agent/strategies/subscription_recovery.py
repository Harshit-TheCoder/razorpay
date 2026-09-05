from typing import Dict, Any
from app.agent.strategies.base import RecoveryStrategy

class SubscriptionRecoveryStrategy(RecoveryStrategy):
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["enriched_data"] = {
            "retry_attempts": context.get("retry_attempts", 1),
            "subscription_age_months": 12,
            "previous_failures": 0
        }
        return context

    def get_system_prompt(self) -> str:
        return """You are evaluating SUBSCRIPTION RECOVERY.
Analyze retry attempts and subscription age.
Allowed actions:
- 'retry_payment': If this is the first failure.
- 'send_email': If we have already retried, remind the user to update their card.
- 'escalate': If a long-term VIP subscription is about to churn.
Output the exact JSON matching the schema."""
