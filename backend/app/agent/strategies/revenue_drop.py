from typing import Dict, Any
from app.agent.strategies.base import RecoveryStrategy

class RevenueDropStrategy(RecoveryStrategy):
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["enriched_data"] = {
            "anomaly_type": "product_revenue_drop",
            "deviation_pct": -15.5,
            "affected_category": "electronics"
        }
        return context

    def get_system_prompt(self) -> str:
        return """You are evaluating a PRODUCT REVENUE DROP anomaly.
Analyze the deviation from the baseline.
Allowed actions:
- 'generate_report': To inform the merchant with a detailed breakdown.
- 'escalate': If the deviation is critical (> 20%).
- 'ignore': If the deviation is within expected seasonal variance.
Output the exact JSON matching the schema."""
