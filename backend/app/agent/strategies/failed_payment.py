from typing import Dict, Any
from app.agent.strategies.base import RecoveryStrategy

class FailedPaymentStrategy(RecoveryStrategy):
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # In a real scenario, this would query the PaymentRepository
        # and fetch merchant error frequency stats.
        context["enriched_data"] = {
            "error_source": context.get("error_source", "bank"),
            "merchant_error_frequency": "high",
            "historical_success_rate": 0.45
        }
        return context

    def get_system_prompt(self) -> str:
        return """You are evaluating a FAILED PAYMENT.
Analyze the error frequency and historical success rate.
Allowed actions:
- 'retry_payment': If failure is temporary and success rate is high.
- 'create_payment_link': If the bank blocked the transaction, offer an alternate payment method via a link.
- 'escalate': For repeated high-value failures.
Output the exact JSON matching the schema."""
