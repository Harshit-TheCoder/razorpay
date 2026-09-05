from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class AuditLogEntry(BaseModel):
    action: str
    actor: str = "system"
    case_id: Optional[str] = None
    merchant_id: Optional[str] = None
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
