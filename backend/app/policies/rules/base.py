from abc import ABC, abstractmethod
from app.recovery.schemas import ActionProposal

class BaseRule(ABC):
    """
    Base class for all policy rules.
    If a rule evaluates to False, the action is blocked.
    """
    
    @abstractmethod
    async def evaluate(self, merchant_id: str, action: ActionProposal) -> bool:
        pass
    
    @property
    @abstractmethod
    def rule_name(self) -> str:
        pass
