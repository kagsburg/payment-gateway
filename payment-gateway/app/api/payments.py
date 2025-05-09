from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.schema import PaymentRequest, PaymentResponse
from app.services.payment import process_payment, check_payment_status,get_all_transactions
from app.models.database import get_db

router = APIRouter()
# post payment request
@router.post("/payments", response_model=PaymentResponse)
async def initiate_payment(payment_request: PaymentRequest,db: Session = Depends(get_db)):
    result= await process_payment(payment_request, db)
    if not result:
        raise HTTPException(status_code=400, detail="Transaction failed")
    return result

# checkout transaction status
@router.get("/payments/{transaction_id}", response_model=PaymentResponse)
async def get_payment_status(transaction_id: str,db: Session = Depends(get_db)):
    result = await check_payment_status(transaction_id, db)
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result