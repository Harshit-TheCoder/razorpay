from pydantic import BaseModel

class RecoveryMetricsDTO(BaseModel):
    merchant_id: str
    total_cases: int
    unresolved_cases: int
    recovered_cases: int
    recovery_rate: float
    revenue_at_risk: float
    revenue_recovered: float
