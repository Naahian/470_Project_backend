from sqlalchemy.orm import Session
from app.model.transaction_model import KTransaction, Sell, Order
from app.schema.transaction_schema import *


def get_transactions(db:Session, skip:int, limit:int):
    return db.query(KTransaction).order_by(KTransaction.timestamp.desc()).offset(skip).limit(limit).all();

def get_transaction_by_id(db:Session, transaction_id:int):
    transaction = db.query(KTransaction).filter(transaction_id == KTransaction.id).first()
    return transaction

def create_transaction(db: Session, transaction: TransactionCreate):
    transaction_type_str = transaction.type.value
    
    db_transaction = KTransaction(
        total_amount=transaction.total_amount,
        type=transaction_type_str,
        user_id=transaction.user_id,
        
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction



# Sell CRUD
def create_sell(db: Session, sell: SellCreate):
    db_sell = Sell(**sell.dict())
    db.add(db_sell)
    db.commit()
    db.refresh(db_sell)
    return db_sell
    

def get_sells(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sell).offset(skip).limit(limit).all()

def get_sell_by_id(db: Session, sell_id: int):
    return db.query(Sell).filter(Sell.id == sell_id).first()

def delete_sell(db: Session, sell_id: int):
    db_sell = db.query(Sell).filter(Sell.id == sell_id).first()
    if db_sell:
        db.delete(db_sell)
        db.commit()
    return db_sell



# Order CRUD
def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()

def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        update_data = order_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)
        db.commit()
        db.refresh(order)
        return order
    return None

def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order

