import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, DateTime
from datetime import datetime
from app.core.db.session import Base

class RecoveryCase(Base):
    __tablename__ = "recovery_cases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False)
    scenario_type = Column(String, nullable=False) # e.g., 'A', 'B', 'C'
    source_ref = Column(String, nullable=False) # polymorphic, e.g., payment_id or checkout_id
    amount = Column(Integer, default=0) # Value at risk in paise (e.g. 1000 = 10.00 INR)
    state = Column(String, nullable=False) # DETECTED, INVESTIGATING, DIAGNOSED...
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    audit_ref = Column(String, nullable=True) # Link to MongoDB audit log

class RecoveryAttempt(Base):
    __tablename__ = "recovery_attempts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("recovery_cases.id"), nullable=False)
    attempt_number = Column(Integer, nullable=False)
    action_type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    executed_at = Column(DateTime, default=datetime.utcnow)
    result = Column(JSON, nullable=True)
    version = Column(Integer, default=1) # Optimistic locking
