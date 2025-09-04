from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import math

from database import get_db
from app.crud import category_crud as crud
from app.schema.category_schema import (
    CategoryCreate, 
    CategoryUpdate, 
    CategoryResponse, 
    CategoryWithProducts,
    CategoryListResponse
)
from app.routes.services import get_current_active_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/create", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)  
):
    try:
        return crud.create_category(db=db, category=category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=CategoryListResponse)
def get_categories(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get all categories with pagination"""
    skip = (page - 1) * per_page
    categories = crud.get_categories(db=db, skip=skip, limit=per_page)
    total = crud.get_categories_count(db=db)
    total_pages = math.ceil(total / per_page)
    
    return CategoryListResponse(
        categories=categories,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )



@router.get("/{category_id}", response_model=CategoryWithProducts)
def get_category_with_products(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = crud.get_category(db=db, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    try:
        updated_category = crud.update_category(
            db=db, 
            category_id=category_id, 
            category_update=category_update
        )
        if not updated_category:
            raise HTTPException(status_code=404, detail="Category not found")
        return updated_category
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)  # Add authentication if needed
):
    try:
        deleted = crud.delete_category(db=db, category_id=category_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Category not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


