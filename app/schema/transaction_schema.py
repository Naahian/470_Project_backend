from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal
from enum import Enum


class TransactionType(str, Enum):
    SELL = "SELL"
    ORDER = "ORDER"


# Transaction
class TransactionBase(BaseModel):
    total_amount: float = Field(..., ge=0, description="Total amount of the transaction")
    user_id: int = Field(..., description="ID of the user associated with the transaction")


class TransactionCreate(BaseModel):
    user_id: int
    type: TransactionType
    total_amount: Decimal


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    total_amount: Decimal

    class Config:
        orm_mode = True


class TransactionDelete(BaseModel):
    id: int



# Order
class OrderBase(TransactionBase):
    supplier_id: int = Field(..., description="ID of the supplier")
    payment_id: str = Field(..., description="ID of the payment")
    quantity: int = Field(..., ge=1, description="Quantity of items")
    delivery_date: datetime = Field(..., description="Expected delivery date")

class OrderCreate(OrderBase):
    type: TransactionType = Field(default=TransactionType.ORDER, description="Transaction type")

class OrderUpdate(BaseModel):
    total_amount: Optional[float] = Field(None, ge=0, description="Total amount of the transaction")
    supplier_id: Optional[int] = Field(None, description="ID of the supplier")
    payment_id: Optional[str] = Field(None, description="ID of the payment")
    quantity: Optional[int] = Field(None, ge=1, description="Quantity of items")
    delivery_date: Optional[datetime] = Field(None, description="Expected delivery date")
    is_delivered: Optional[bool] = Field(None, description="Delivery status")

class OrderResponse(OrderBase):
    id: int
    timestamp: datetime
    type: TransactionType
    is_delivered: bool
    total_amount: float
    user_id: int
    
    class Config:
        orm_mode = True


# Sell 
class SellBase(TransactionBase):
    user_id: int
    total_amount: Optional[float] = Field(None, ge=0, description="Total amount of the transaction")
    products: List[int] = Field(..., description="List of product IDs")

class SellCreate(SellBase):
    type: TransactionType = Field(default=TransactionType.ORDER, description="Transaction type")

class SellResponse(SellBase):
    id: int
    user_id: int
    timestamp: datetime
    type: TransactionType
    total_amount:float
    products:List[int]
    
    class Config:
        orm_mode = True

