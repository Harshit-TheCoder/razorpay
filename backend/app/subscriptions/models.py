import uuid
from sqlalchemy import Column, String, ForeignKey, Integer
from app.core.db.session import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    razorpay_subscription_id = Column(String, nullable=True)
    type = Column(String, nullable=True)
    status = Column(String, nullable=False)

class SubscriptionCharge(Base):
    __tablename__ = "subscription_charges"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    subscription_id = Column(String, ForeignKey("subscriptions.id"), nullable=False)
    razorpay_invoice_id = Column(String, nullable=True)
    status = Column(String, nullable=False)
    attempt_number = Column(Integer, default=1)
