from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.model.category_model import Category
from app.schema.category_schema import CategoryCreate, CategoryUpdate
from typing import List, Optional

def create_category( db: Session, category: CategoryCreate):
    """Create a new category"""
    try:
        print(f"category {category}")
        db_category = Category(
            name=category.name,
            quantity=0,
            imageNo=category.imageNo
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Category with name '{category.name}' already exists")

def get_category( db: Session, category_id: int) -> Optional[Category]:
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories( db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
    # for each category get total product that are sold.
    return  db.query(Category).offset(skip).limit(limit).all()

def get_categories_count( db: Session) -> int:
    return db.query(Category).count()

def update_category( db: Session, category_id: int, category_update: CategoryUpdate) -> Optional[Category]:
    db_category = get_category(db, category_id)
    if not db_category:
        return None  
    try:
        
        update_data = category_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Category with name '{category_update.name}' already exists")

def delete_category( db: Session, category_id: int) -> bool:
    db_category = get_category(db, category_id)
    if not db_category:
        return False

    if db_category.products:
        raise ValueError("Cannot delete category with associated products")
    
    db.delete(db_category)
    db.commit()
    return True
    
   

