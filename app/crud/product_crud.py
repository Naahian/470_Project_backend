from sqlalchemy.orm import Session
from app.model.product_model import Product
from app.schema.product_schema import ProductCreate
from app.model.category_model import Category

def create_product(db:Session, product:ProductCreate):
    Category()
    db_product = Product(
        name=product.name.lower(),
        description=product.description,
        quantity=product.quantity,
        price=product.price,
        category_id=product.category_id,
        supplier_id=product.supplier_id,
        created_by=product.created_by
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

def read_products(db:Session, skip:int=0, limit:int=100):
    products = db.query(Product).all()
    return products

def get_product_by_id(db:Session, product_id:int):
    product = db.query(Product).filter(product_id == Product.id).first()
    return product

def get_product_by_name(db:Session, product_name:str):
    
    product = db.query(Product).filter(product_name.lower() == Product.name).first()
    return product

def update_product(db:Session, product_id:int, product:ProductCreate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if(db_product):
        update_product = product.dict(exclude_unset=True)
        for field, value in update_product.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product
    
def delete_product(db:Session, product_id:int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if(db_product):
        db.delete(db_product)
        db.commit()
    return db_product

