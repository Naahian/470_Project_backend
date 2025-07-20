from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base  # Assuming your Base is defined in database.py

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(100), nullable=True)

    # Relationships
    products = relationship("Product", back_populates="category")
