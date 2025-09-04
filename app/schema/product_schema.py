from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.model.product_model import Product


class ProductBase(BaseModel):
    category_id: Optional[int]
    supplier_id: Optional[int]
    category_name: Optional[str]
    supplier_name: Optional[str]


class ProductCreate(ProductBase):
    quantity: Optional[int] = Field(default=1)


class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    in_stock: bool

    class Config:
        orm_mode = True
    
    @classmethod
    def from_productModel(cls, product: Product) -> "ProductResponse":
        return cls(
            id=product.id,
            created_at=product.created_at,
            updated_at=product.updated_at,
            in_stock=product.in_stock,
            # Include ALL fields from ProductBase
            category_id=product.category_id,
            supplier_id=product.supplier_id,
            category_name=product.category_name,  # This exists as a column
            supplier_name=product.supplier_name,   # This exists as a column
        )
    


class ProductListResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class ProductDelete(BaseModel):
    id: int
