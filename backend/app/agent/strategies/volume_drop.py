from typing import Dict, Any
from app.agent.strategies.base import RecoveryStrategy

class VolumeDropStrategy(RecoveryStrategy):
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["enriched_data"] = {
            "anomaly_type": "transaction_volume_drop",
            "deviation_pct": -25.0,
            "time_window_hours": 1
        }
        return context

    def get_system_prompt(self) -> str:
        return """You are evaluating a TRANSACTION VOLUME DROP.
Analyze the volume deviation. This often indicates a platform issue or a payment gateway outage.
Allowed actions:
- 'escalate': Always escalate significant volume drops to on-call engineers.
- 'generate_report': If the drop is minor.
Output the exact JSON matching the schema."""
