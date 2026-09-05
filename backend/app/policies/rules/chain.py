import structlog
from typing import List
from app.recovery.schemas import ActionProposal
from .base import BaseRule
from .frequency_rule import FrequencyRule
from .amount_rule import AmountRule

logger = structlog.get_logger(__name__)

class PolicyEngine:
    def __init__(self):
        # Register active rules here
        self.rules: List[BaseRule] = [
            FrequencyRule(),
            AmountRule()
        ]

    async def evaluate(self, merchant_id: str, proposed_action: ActionProposal) -> bool:
        """
        Iterates through all active rules. If any rule returns False, 
        the action is blocked immediately.
        """
        for rule in self.rules:
            is_allowed = await rule.evaluate(merchant_id, proposed_action)
            if not is_allowed:
                logger.warning(f"Action blocked by policy rule: {rule.rule_name}", action_type=proposed_action.action_type)
                return False
                
        return True
