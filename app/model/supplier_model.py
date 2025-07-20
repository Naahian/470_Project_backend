from datetime import datetime
from sqlalchemy import  Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base    



class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_info = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", back_populates="supplier")
