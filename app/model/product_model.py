from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
 
    transactions = relationship("KTransaction", back_populates="product")
    creator = relationship("User", back_populates="created_products")
    category = relationship("Category", back_populates="products")  # if you have Category model
    supplier = relationship("Supplier", back_populates="products")  # if you have Supplier model