import uuid
from sqlalchemy import Column, String, ForeignKey
from app.core.db.session import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    razorpay_order_id = Column(String, nullable=True)
    status = Column(String, nullable=False)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False)
    order_id = Column(String, ForeignKey("orders.id"), nullable=True)
    razorpay_payment_id = Column(String, nullable=True)
    status = Column(String, nullable=False)
    error_code = Column(String, nullable=True)
    error_reason = Column(String, nullable=True)
    error_source = Column(String, nullable=True)
