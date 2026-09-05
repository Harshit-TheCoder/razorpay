import uuid
from sqlalchemy import Column, String, JSON, DateTime
from datetime import datetime
from app.core.db.session import Base

class RawEvent(Base):
    __tablename__ = "events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False)
    source = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
    external_event_id = Column(String, nullable=False, unique=True)
