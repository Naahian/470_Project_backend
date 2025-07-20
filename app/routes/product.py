from fastapi import  APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.services import get_current_active_user, require_admin
from database import get_db
from app.model.user_model import User
from app.crud import product_crud as crud
from app.schema.product_schema import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get('/', response_model=None) 
def get_products(
    skip:int =0 ,
    limit:int=100,
    db:Session = Depends(get_db),
    current_user:User=Depends(get_current_active_user),
):
    products = crud.read_products(db,skip=skip,limit=limit)
    return products

@router.get('/{id}', response_model=ProductResponse) 
def get_product(
    id:str,
    db:Session = Depends(get_db),
    current_user:User=Depends(get_current_active_user)
):
    return crud.get_product_by_id(db, product_id=id)


@router.post('/create', response_model=ProductResponse) 
def create_product(
    product:ProductCreate,
    db:Session = Depends(get_db),
    current_user:User=Depends(require_admin),
):
    db_product = crud.get_product_by_name(db,product_name=product.name)
    if(db_product):
        raise HTTPException(status_code=400,detail="product already exists.")
    
    product = crud.create_product(db, product)
    return product
    

@router.delete('/{product_id}', response_model=ProductResponse)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    db_product = crud.get_product_by_id(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return crud.delete_product(db, product_id=product_id)



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


