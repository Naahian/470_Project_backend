
from datetime import datetime
from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base    

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    method = Column(String(50)) 
    paid_at = Column(DateTime, default=datetime.utcnow)
