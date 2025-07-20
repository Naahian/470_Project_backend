from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schema.product_schema import ProductResponse


class SupplierBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Supplier name")
    contact_info: Optional[str] = Field(None, description="Supplier contact information")


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Supplier name")
    contact_info: Optional[str] = Field(None, description="Supplier contact information")


class SupplierResponse(SupplierBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SupplierSummary(BaseModel):
    """Summary response with product count"""
    id: int
    name: str
    contact_info: Optional[str]
    created_at: datetime
    product_count: int
    
    class Config:
        from_attributes = True


class SupplierListResponse(BaseModel):
    suppliers: List[SupplierResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class SupplierSummaryListResponse(BaseModel):
    suppliers: List[SupplierSummary]
    total: int
    page: int
    per_page: int
    total_pages: int