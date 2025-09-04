import math
from fastapi import  APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.routes.services import get_current_active_user, require_admin
from app.schema.category_schema import CategoryUpdate
from database import get_db
from app.model.user_model import User
from app.crud import product_crud as crud
from app.crud import category_crud
from app.schema.product_schema import ProductCreate, ProductListResponse, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    skip = (page - 1) * per_page
    total = crud.get_products_count(db)
    total_pages = math.ceil(total / per_page) if per_page > 0 else 0
    products = crud.read_products(db, skip=skip, limit=per_page)
    products = [ProductResponse.from_productModel(product) for product in products]
    
    return ProductListResponse(
        products=products,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get('/{id}', response_model=ProductResponse) 
def get_product(
    id:str,
    db:Session = Depends(get_db),
    current_user:User=Depends(get_current_active_user)
):
    return crud.get_product_by_id(db, product_id=id)


@router.post('/create') 
def create_product(
    product:ProductCreate,
    db:Session = Depends(get_db),
    current_user:User=Depends(require_admin),
):
    for _ in range(product.quantity):
        crud.create_product(db, product)
        categoryQuantity = category_crud.get_category(db, product.category_id).quantity + 1
        category_crud.update_category(db, product.category_id,  CategoryUpdate(quantity=categoryQuantity))
    
    return {"msg":"success"}
    

@router.delete('/{product_id}', response_model=ProductResponse)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.") 
    
    product = crud.delete_product(db, product_id=product_id)
    newQuantity = category_crud.get_category(db, product.category_id).quantity - 1
    category_crud.update_category(db, product.category_id, CategoryUpdate(quantity=newQuantity))

    return product



@router.put('/{product_id}', response_model=ProductResponse)
def update_product(
    product_id: str,
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return crud.update_product(db, product_id=product_id, product=product)


