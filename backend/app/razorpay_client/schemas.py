from pydantic import BaseModel
from typing import Dict, Any, Optional

class RazorpayExecutionResponse(BaseModel):
    success: bool
    raw_response: Dict[str, Any]
    error_message: Optional[str] = None
