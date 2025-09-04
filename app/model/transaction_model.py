from datetime import datetime
from sqlalchemy import DECIMAL, JSON, Column, ForeignKey, Integer, String, DateTime, Enum, Boolean, ARRAY
from sqlalchemy.orm import relationship
from database import Base    
import enum


class TransactionType(enum.Enum):
    SELL = "SELL"
    ORDER = "ORDER"


class KTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(DECIMAL(10, 2))
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(Enum(TransactionType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="transactions")

class Order(KTransaction):
    __tablename__ = "orders"

    id = Column(Integer, ForeignKey("transactions.id"), primary_key=True)  
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    payment_id = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    is_delivered = Column(Boolean, default=False)
    
     
class Sell(KTransaction):
    __tablename__ = "sells"
    
    id = Column(Integer, ForeignKey("transactions.id"), primary_key=True)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    products = Column(JSON)
