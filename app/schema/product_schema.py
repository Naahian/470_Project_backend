from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    category_id: Optional[int]
    supplier_id: Optional[int]
    category_name: Optional[str]
    supplier_name: Optional[str]


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    in_stock: bool

    class Config:
        orm_mode = True


class ProductDelete(BaseModel):
    id: int
