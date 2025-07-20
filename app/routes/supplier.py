from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import math

from database import get_db
from app.crud import supplier_crud
from app.schema.supplier_schema import (
    SupplierCreate, 
    SupplierUpdate, 
    SupplierResponse, 
    SupplierListResponse,
)
from app.routes.services import  require_admin  

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.post("/create", response_model=SupplierResponse, status_code=201)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Create a new supplier"""
    return supplier_crud.create_supplier(db=db, supplier=supplier)


@router.get("/", response_model=SupplierListResponse)
def get_suppliers(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get all suppliers with pagination"""
    skip = (page - 1) * per_page
    suppliers = supplier_crud.get_suppliers(db=db, skip=skip, limit=per_page)
    total = supplier_crud.get_suppliers_count(db=db)
    total_pages = math.ceil(total / per_page)
    
    return SupplierListResponse(
        suppliers=suppliers,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )




@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific supplier by ID"""
    supplier = supplier_crud.get_supplier(db=db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier




@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  
):
    """Update a supplier"""
    updated_supplier = supplier_crud.update_supplier(
        db=db, 
        supplier_id=supplier_id, 
        supplier_update=supplier_update
    )
    if not updated_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated_supplier


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin) 
):
    """Delete a supplier"""
    try:
        deleted = supplier_crud.delete_supplier(db=db, supplier_id=supplier_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Supplier not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

