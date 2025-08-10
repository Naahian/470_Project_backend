from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base 

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    imageNo = Column(Integer,nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="category")
