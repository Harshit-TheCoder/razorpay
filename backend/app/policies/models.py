import uuid
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from app.core.db.session import Base

class PolicyProfile(Base):
    __tablename__ = "policies"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False, unique=True)
    max_retries = Column(Integer, default=2)
    max_transaction_amount = Column(Integer, default=10000)
    max_contacts = Column(Integer, default=3)
    recovery_window_days = Column(Integer, default=7)
    require_human_approval = Column(Boolean, default=False)
