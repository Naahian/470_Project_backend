from pydantic import BaseModel, Field
from typing import Optional, List
from app.schema.product_schema import ProductResponse

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Category name")
    description: Optional[str] = Field(None, max_length=100, description="Category description")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Category name")
    description: Optional[str] = Field(None, max_length=100, description="Category description")


class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True


class CategoryWithProducts(CategoryResponse):
    products: List['ProductResponse'] = []
    
    class Config:
        from_attributes = True


# For pagination response
class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
    total: int
    page: int
    per_page: int
    total_pages: int