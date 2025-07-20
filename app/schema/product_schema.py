from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    category: Optional[str]
    description: Optional[str]
    

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    quantity: int
    price: Decimal
    category_id:int
    supplier_id: int
    created_by: int


class ProductResponse(BaseModel):
    id:int
    name: str
    description: Optional[str]
    quantity: int
    price: Decimal
    supplier_id: int
    created_by: int
    category_id:int

    class Config:
        orm_mode = True


class ProductDelete(BaseModel):
    id: int