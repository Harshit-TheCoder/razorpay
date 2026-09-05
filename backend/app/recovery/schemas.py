from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class RecoveryCaseCreateDTO(BaseModel):
    merchant_id: str
    scenario_type: str
    source_ref: str
    state: str = "DETECTED"

class RecoveryCaseResponseDTO(RecoveryCaseCreateDTO):
    id: str
    opened_at: datetime
    closed_at: Optional[datetime] = None

class ActionProposal(BaseModel):
    case_id: str
    action_type: str
    payload: Dict[str, Any]
    rationale_text: str

class RecoveryAttemptResponseDTO(BaseModel):
    id: str
    case_id: str
    attempt_number: int
    action_type: str
    status: str
    executed_at: datetime
    result: Optional[Dict[str, Any]] = None
    version: int
