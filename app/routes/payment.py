import os
from typing import Any, Dict
import uuid
import requests
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.logger import logger
from app.schema.payment_schema import PaymentInitRequest, PaymentInitResponse, PaymentResponse


SSLCOMMERZ_STORE_ID = os.getenv("SSLCOMMERZ_STORE_ID", "your_store_id")
SSLCOMMERZ_STORE_PASSWORD = os.getenv("SSLCOMMERZ_STORE_PASSWORD", "your_store_password")
SSLCOMMERZ_IS_SANDBOX = os.getenv("SSLCOMMERZ_SANDBOX", "true").lower() == "true"

# URLs
if SSLCOMMERZ_IS_SANDBOX:
    SSLCOMMERZ_SESSION_URL = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
    SSLCOMMERZ_VALIDATION_URL = "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"
else:
    SSLCOMMERZ_SESSION_URL = "https://securepay.sslcommerz.com/gwprocess/v4/api.php"
    SSLCOMMERZ_VALIDATION_URL = "https://securepay.sslcommerz.com/validator/api/validationserverAPI.php"

router = APIRouter(prefix='/payment')
emulator_url = "http://10.0.2.2:8000"
local_url = "http://127.0.0.1:8000"


@router.post("/init", response_model=PaymentInitResponse)
async def init_payment(payment_request: PaymentInitRequest):
    try:
        transaction_id = f"TXN_{uuid.uuid4().hex[:10].upper()}"
        
        payload = {
            'store_id': SSLCOMMERZ_STORE_ID,
            'store_passwd': SSLCOMMERZ_STORE_PASSWORD,
            'total_amount': str(payment_request.amount),
            'currency': payment_request.currency,
            'tran_id': transaction_id,
            'success_url': f"{os.getenv('BASE_URL', 'http://localhost:8000')}/payment/success",
            'fail_url': f"{os.getenv('BASE_URL', 'http://localhost:8000')}/payment/fail",
            'cancel_url': f"{os.getenv('BASE_URL', 'http://localhost:8000')}/payment/cancel",
            'ipn_url': f"{os.getenv('BASE_URL', 'http://localhost:8000')}/payment/ipn",
            
            #customer information
            'cus_name': payment_request.customer_name,
            'cus_email': payment_request.customer_email,
            'cus_add1': payment_request.customer_address,
            'cus_city': payment_request.customer_city,
            'cus_country': payment_request.customer_country,
            'cus_phone': payment_request.customer_phone,
            
            #product information
            'product_name': payment_request.product_name,
            'product_category': payment_request.product_category,
            'product_profile': payment_request.product_profile,
            
            #shipping info
            'shipping_method':'NO',
            
        }
        
        response = requests.post(
            SSLCOMMERZ_SESSION_URL,
            data=payload,
            timeout=30
        )

        return process_response(response, transaction_id)
        

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
    


def process_response(response, transaction_id):
    result = None;
    if response.status_code == 200:
        result = response.json()
        
        if result.get('status') == 'SUCCESS':           
            return PaymentInitResponse(
                status="success",
                message="Payment session created successfully",
                gateway_url=result.get('GatewayPageURL'),
                session_key=result.get('sessionkey'),
                transaction_id=transaction_id
            )
        else:
            return PaymentInitResponse(
                status="failed",
                message=f"Failed to create payment session: {result.get('failedreason', 'Unknown error')}"
            )
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to communicate with payment gateway"
        )
    
    

@router.post("/success", response_model=PaymentResponse)
async def payment_success(request: Request):
    """
    Handle successful payment callback from SSLCommerz
    This endpoint receives POST data from SSLCommerz redirect
    """
    
    try:
        form_data = await request.form()
        success_data = dict(form_data)
        
        logger.info(f"Payment success received: {success_data}")
        
        # Extract required parameters
        tran_id = success_data.get('tran_id')
        val_id = success_data.get('val_id')
        amount = success_data.get('amount')
        
        if not all([tran_id, val_id, amount]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required parameters: tran_id, val_id, or amount"
            )
        
        # Validate payment with SSLCommerz
        validation_result = await validate_payment(val_id)
        
        if validation_result.get('status') in ['VALID', 'VALIDATED']:
            # Payment is valid - update your database here
            logger.info(f"Payment validated successfully for transaction: {tran_id}")
            
            # TODO: Implement your database update logic
            # Example: await update_payment_status(tran_id, "success", validation_result)
            
            return PaymentResponse(
                success=True,
                message="Payment completed successfully",
                transaction_id=tran_id,
                status="success",
                validation_data=validation_result
            )
        else:
            logger.warning(f"Payment validation failed for transaction: {tran_id}")
            return PaymentResponse(
                success=False,
                message="Payment validation failed",
                transaction_id=tran_id,
                status="validation_failed"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in payment success handler: {str(e)}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/fail", response_model=PaymentResponse)
async def payment_fail(request: Request):
    """
    Handle failed payment callback from SSLCommerz
    This endpoint receives POST data from SSLCommerz redirect
    """
    try:
        form_data = await request.form()
        fail_data = dict(form_data)
        
        logger.warning(f"Payment failed received: {fail_data}")
        
        tran_id = fail_data.get('tran_id')
        error_message = fail_data.get('error', 'Payment failed')
        status_msg = fail_data.get('status', 'failed')
        
        if not tran_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing transaction ID"
            )
        
        # TODO: Update your database - mark payment as failed
        # Example: await update_payment_status(tran_id, "failed", {"error": error_message})
        
        logger.info(f"Payment marked as failed for transaction: {tran_id}")
        
        return PaymentResponse(
            success=False,
            message=error_message,
            transaction_id=tran_id,
            status=status_msg
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in payment fail handler: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/cancel", response_model=PaymentResponse)
async def payment_cancel(request: Request):
    """
    Handle cancelled payment callback from SSLCommerz
    This endpoint receives POST data from SSLCommerz redirect
    """
    try:
        form_data = await request.form()
        cancel_data = dict(form_data)
        
        logger.info(f"Payment cancelled received: {cancel_data}")
        
        tran_id = cancel_data.get('tran_id')
        status_msg = cancel_data.get('status', 'cancelled')
        
        if not tran_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing transaction ID"
            )
        
        # TODO: Update your database - mark payment as cancelled
        # Example: await update_payment_status(tran_id, "cancelled", {})
        
        logger.info(f"Payment marked as cancelled for transaction: {tran_id}")
        
        return PaymentResponse(
            success=False,
            message="Payment was cancelled by user",
            transaction_id=tran_id,
            status=status_msg
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in payment cancel handler: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
    

async def validate_payment(val_id: str) -> Dict[str, Any]:
    """
    Validate payment with SSLCommerz
    """
    try:
        validation_url = f"{SSLCOMMERZ_VALIDATION_URL}?val_id={val_id}&store_id={SSLCOMMERZ_STORE_ID}&store_passwd={SSLCOMMERZ_STORE_PASSWORD}&format=json"
        
        response = requests.get(validation_url, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Validation request failed: {response.status_code}")
            return {"status": "ERROR", "message": "Validation failed"}
            
    except Exception as e:
        logger.error(f"Error in payment validation: {str(e)}")
        return {"status": "ERROR", "message": str(e)}
