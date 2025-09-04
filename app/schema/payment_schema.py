
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class PaymentInitRequest(BaseModel):
    amount: float
    currency: str = "BDT"
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_address: str
    customer_city: str
    customer_country: str = "Bangladesh"
    product_name: str
    product_category: str = "General"
    product_profile: str = "general"


class PaymentInitResponse(BaseModel):
    status: str
    message: str
    gateway_url: Optional[str] = None
    session_key: Optional[str] = None
    transaction_id: Optional[str] = None



    # Request/Response Schemas
class PaymentSuccessRequest(BaseModel):
    tran_id: str = Field(..., description="Transaction ID from SSLCommerz")
    val_id: str = Field(..., description="Validation ID from SSLCommerz")
    amount: str = Field(..., description="Payment amount")
    card_type: Optional[str] = Field(None, description="Type of card used")
    store_amount: Optional[str] = Field(None, description="Store amount")
    card_no: Optional[str] = Field(None, description="Masked card number")
    bank_tran_id: Optional[str] = Field(None, description="Bank transaction ID")
    status: Optional[str] = Field(None, description="Payment status")
    tran_date: Optional[str] = Field(None, description="Transaction date")
    currency: Optional[str] = Field(None, description="Currency type")
    card_issuer: Optional[str] = Field(None, description="Card issuer bank")
    card_brand: Optional[str] = Field(None, description="Card brand")
    card_issuer_country: Optional[str] = Field(None, description="Card issuer country")
    currency_type: Optional[str] = Field(None, description="Currency type")
    currency_amount: Optional[str] = Field(None, description="Currency amount")

class PaymentFailRequest(BaseModel):
    tran_id: str = Field(..., description="Transaction ID from SSLCommerz")
    error: Optional[str] = Field("Payment failed", description="Error message")
    status: Optional[str] = Field(None, description="Payment status")

class PaymentCancelRequest(BaseModel):
    tran_id: str = Field(..., description="Transaction ID from SSLCommerz")
    status: Optional[str] = Field(None, description="Payment status")

class PaymentResponse(BaseModel):
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    transaction_id: str = Field(..., description="Transaction ID")
    status: Optional[str] = Field(None, description="Payment status")

class PaymentValidationResponse(BaseModel):
    status: str
    tran_id: str
    val_id: str
    amount: str
    store_amount: str
    card_type: str
    card_no: str
    currency: str
    bank_tran_id: str
    card_issuer: str
    card_brand: str
    card_issuer_country: str
    card_issuer_country_code: str
    currency_type: str
    currency_amount: str
    currency_rate: str
    base_fair: str
    value_a: str
    value_b: str
    value_c: str
    value_d: str
    risk_level: str
    risk_title: str
