from abc import ABC, abstractmethod
from typing import Dict, Any
from app.agent.schemas import AgentAction

class RecoveryStrategy(ABC):
    @abstractmethod
    async def collect_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather all necessary information for this specific scenario."""
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the scenario-specific prompt instructions for the LLM."""
        pass
