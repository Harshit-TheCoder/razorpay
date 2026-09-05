from pydantic import BaseModel, Field
from typing import Dict, Any, List

class AgentAction(BaseModel):
    action_type: str = Field(description="The type of action to take (e.g., 'send_email', 'retry_payment', 'create_ticket')")
    payload: Dict[str, Any] = Field(description="The parameters required for this action")
    rationale_text: str = Field(description="Explanation of why this action was chosen")

class AgentState(BaseModel):
    scenario_type: str
    context: Dict[str, Any]
    messages: List[Any] = []
    proposed_action: AgentAction | None = None
