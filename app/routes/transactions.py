from fastapi import APIRouter, HTTPException, Depends
from typing import List, Union
from app.crud import transaction_crud
from app.model.transaction_model import Sell, TransactionType
from app.schema.transaction_schema import OrderCreate, OrderResponse, OrderUpdate, SellCreate, SellResponse, TransactionResponse, TransactionCreate
from database import get_db
from sqlalchemy.orm import Session


# Transaction
router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
    ):
    return transaction_crud.get_transactions(db, skip=skip, limit=limit)


@router.post("/create", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
   ):
    return transaction_crud.create_transaction(db, transaction)



@router.delete("/{transaction_id}", response_model=dict)
def delete_transaction(transaction_id: int):
    deleted = transaction_crud.delete_transaction(transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted"}



# ORDER
@router.get("/orders/", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return transaction_crud.get_orders(db, skip=skip, limit=limit)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = transaction_crud.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/orders/create", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
):
    return transaction_crud.create_order(db, order)

@router.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order: OrderUpdate,
    order_id:int,
    db: Session = Depends(get_db)
):
    return transaction_crud.update_order(db,order_id,order)

@router.delete("/orders/{order_id}", response_model=dict)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order by ID"""
    deleted = transaction_crud.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}



# SELL
@router.get("/sells/", response_model=List[SellResponse])
def get_sells(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    return transaction_crud.get_sells(db, skip=skip, limit=limit)


@router.get("/sells/{sell_id}", response_model=SellResponse)
def get_sell(sell_id: int, db: Session = Depends(get_db)):
    sell = transaction_crud.get_sell_by_id(db, sell_id)
    if not sell:
        raise HTTPException(status_code=404, detail="Sell not found")
    return sell


@router.post("/sells/create", response_model=SellResponse)
def create_sell(
    sell: SellCreate,
    db: Session = Depends(get_db),
):
    return transaction_crud.create_sell(db, sell)


@router.delete("/sells/{sell_id}", response_model=dict)
def delete_sell(sell_id: int, db: Session = Depends(get_db)):
    deleted = transaction_crud.delete_sell(db, sell_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sell not found")
    return {"detail": "Sell deleted"}


# Single Transaction Detail
@router.get("/{id}", response_model=Union[SellResponse,OrderResponse])
def get_transaction(id: int, db: Session = Depends(get_db)):
    transaction = transaction_crud.get_transaction_by_id(db, id)
    if transaction.type == TransactionType.SELL:
        return transaction_crud.get_sell_by_id(db, id)
    else:
        return transaction_crud.get_order_by_id(db, id)
