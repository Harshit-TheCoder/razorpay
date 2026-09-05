import uuid
from sqlalchemy import Column, String
from app.core.db.session import Base

class Merchant(Base):
    __tablename__ = "merchants"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    razorpay_key_ref = Column(String, nullable=True)
    policy_profile_id = Column(String, nullable=True)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False) # FK left loose for now, or ForeignKey("merchants.id")
    razorpay_customer_id = Column(String, nullable=True)
    contact_prefs = Column(String, nullable=True)

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    merchant_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price = Column(String, nullable=False)
    category = Column(String, nullable=True)
