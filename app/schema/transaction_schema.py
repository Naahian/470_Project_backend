from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from enum import Enum


class TransactionType(str, Enum):
    SELL = "SELL"
    REFILL = "REFILL"


class TransactionCreate(BaseModel):
    product_id: int
    user_id: int
    type: TransactionType
    quantity: int
    total_amount: Decimal


class TransactionResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    type: TransactionType
    quantity: int
    total_amount: Decimal

    class Config:
        orm_mode = True


class TransactionDelete(BaseModel):
    id: int


#Payment

class PaymentCreate(BaseModel):
    transaction_id: int
    amount: Decimal
    method: Optional[str]


class PaymentResponse(BaseModel):
    id: int
    transaction_id: int
    amount: Decimal
    method: Optional[str]

    class Config:
        orm_mode = True


class PaymentDelete(BaseModel):
    id: int