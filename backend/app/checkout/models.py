import uuid
from sqlalchemy import Column, String, ForeignKey, JSON
from app.core.db.session import Base

class CheckoutRecord(Base):
    __tablename__ = "checkout_records"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=True)
    cart_snapshot = Column(JSON, nullable=True)
    status = Column(String, nullable=False) # e.g., 'abandoned', 'recovered'
