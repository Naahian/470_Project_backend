from datetime import datetime
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base    
import enum


class TransactionType(enum.Enum):
    SELL = "SELL"
    REFILL = "REFILL"

#Due to naming conflict of sqlalchemy Transaction class
class KTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_amount = Column(DECIMAL(10, 2))
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    payment = relationship("Payment", back_populates="transaction", uselist=False)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    method = Column(String(50))  # e.g., 'cash', 'card'
    paid_at = Column(DateTime, default=datetime.utcnow)

    transaction = relationship("KTransaction", back_populates="payment")