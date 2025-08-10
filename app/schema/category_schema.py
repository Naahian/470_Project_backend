from pydantic import BaseModel, Field
from typing import Optional, List
from app.schema.product_schema import ProductResponse

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Category name")
    quantity: int = Field(..., ge=0, description="Total quantity available")
    imageNo: Optional[int] = Field(None, description="Image number reference (optional)")

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    quantity: Optional[int] = Field(None, ge=0)
    imageNo: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True  

class CategoryWithProducts(CategoryResponse):
    products: List[ProductResponse] = []

    class Config:
        from_attributes = True

class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
