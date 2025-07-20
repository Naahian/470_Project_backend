from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.model.supplier_model import Supplier
from app.schema.supplier_schema import SupplierCreate, SupplierUpdate
from typing import List, Optional
from datetime import datetime


def create_supplier(db: Session, supplier: SupplierCreate) -> Supplier:
    """Create a new supplier"""
    db_supplier = Supplier(
        name=supplier.name,
        contact_info=supplier.contact_info,
        created_at=datetime.utcnow()
    )
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def get_supplier(db: Session, supplier_id: int) -> Optional[Supplier]:
    """Get a supplier by ID"""
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()


def get_supplier_by_name(db: Session, name: str) -> Optional[Supplier]:
    """Get a supplier by name"""
    return db.query(Supplier).filter(Supplier.name == name).first()


def get_suppliers(db: Session, skip: int = 0, limit: int = 100) -> List[Supplier]:
    """Get all suppliers with pagination"""
    return db.query(Supplier).order_by(Supplier.created_at.desc()).offset(skip).limit(limit).all()


def get_suppliers_count(db: Session) -> int:
    """Get total count of suppliers"""
    return db.query(Supplier).count()


def update_supplier(db: Session, supplier_id: int, supplier_update: SupplierUpdate) -> Optional[Supplier]:
    """Update a supplier"""
    db_supplier = get_supplier(db, supplier_id)
    if not db_supplier:
        return None
    
    # Update only provided fields
    update_data = supplier_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_supplier, field, value)
    
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


def delete_supplier(db: Session, supplier_id: int) -> bool:
    """Delete a supplier"""
    db_supplier = get_supplier(db, supplier_id)
    if not db_supplier:
        return False
    
    # Check if supplier has products
    if db_supplier.products:
        raise ValueError("Cannot delete supplier with associated products")
    
    db.delete(db_supplier)
    db.commit()
    return True


def search_suppliers(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Supplier]:
    """Search suppliers by name or contact info"""
    return db.query(Supplier).filter(
        Supplier.name.ilike(f"%{query}%") | 
        Supplier.contact_info.ilike(f"%{query}%")
    ).order_by(Supplier.created_at.desc()).offset(skip).limit(limit).all()


