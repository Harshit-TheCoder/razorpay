from typing import Dict, Any
from app.agent.strategies.base import RecoveryStrategy

class PremiumRecoveryStrategy(RecoveryStrategy):
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["enriched_data"] = {
            "policy_status": "at_risk",
            "days_to_lapse": 3,
            "historical_payment_success": True
        }
        return context

    def get_system_prompt(self) -> str:
        return """You are evaluating an INSURANCE PREMIUM RECOVERY case.
Analyze the context to prevent a policy lapse.
Allowed actions:
- 'send_reminder': If the policy is at risk but not immediately lapsing, to prompt manual payment.
- 'retry_payment': If the AutoPay failure was temporary.
- 'escalate': If the policy will lapse within 24 hours.
Output the exact JSON matching the schema."""
