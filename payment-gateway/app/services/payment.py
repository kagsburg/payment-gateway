import random
import time
import uuid
import asyncio
from datetime import datetime
from app.models.database import get_db, Transaction,TransactionStatus
from sqlalchemy.orm import Session
import asyncio
from fastapi.responses import JSONResponse

def error_response(message: str, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={"message": message}
    )
def generate_transaction_id():
    return str(uuid.uuid4()).replace('-', '')  # Compact UUID format for MySQL

def determine_transaction_status():
    rand = random.random()
    if rand <= 0.05:
        return TransactionStatus.FAILED, random.choice([
            "Insufficient funds",
            "Invalid payee account",
            "Daily limit exceeded"
        ])
    elif rand <= 0.15:
        return TransactionStatus.PENDING, None
    else:
        return TransactionStatus.SUCCESSFUL, None

def get_status_code(status: TransactionStatus):
    return {
        TransactionStatus.PENDING: 100,
        TransactionStatus.SUCCESSFUL: 200,
        TransactionStatus.FAILED: 400
    }[status]
# logic to process payment
async def process_payment(payment_request, db: Session):
    try:
        start_time = time.time()
        
        status, error_msg = determine_transaction_status()
        now = datetime.utcnow()
        
        transaction = Transaction(
            ref_code=generate_transaction_id(),
            payer_account=payment_request.payer,
            payee_account=payment_request.payee,
            amount=payment_request.amount,
            currency=payment_request.currency,
            payer_reference=payment_request.payer_reference,
            status=status,
            created_at=now,
            updated_at=now,
            error_message=error_msg
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        # Ensure minimum 100ms response time
        elapsed = (time.time() - start_time) * 1000
        if elapsed < 100:
            remaining_delay = (100 - elapsed) / 1000
            await asyncio.sleep(remaining_delay)
        
        return {
            "status_code": get_status_code(status),
            "transaction_reference": transaction.ref_code,
            "message": f"Transaction {status.value.lower()}" + 
                    (f": {error_msg}" if error_msg else "")
        }
    except Exception as e:
        db.rollback()
        return {
            "status_code": 500,
            "transaction_reference": None,
            "message": f"Internal server error: {str(e)}"
        }
# function to get payment status
async def check_payment_status(transaction_id: str, db: Session):
    try:
        transaction = db.query(Transaction).filter(Transaction.ref_code == transaction_id).first()
        if not transaction:
            return None
        
        return {
            "status_code": get_status_code(transaction.status),
            "transaction_reference": transaction.ref_code,
            "message": f"Transaction {transaction.status.value.lower()}" +
                    (f": {transaction.error_message}" if transaction.error_message else "")
        }
    except Exception as e:
        return {
            "status_code": 500,
            "transaction_reference": None,
            "message": f"Internal server error: {str(e)}"
        }
# function to get all transactions
async def get_all_transactions(db:Session):
    try:
        transactions = db.query(Transaction).all()
        if not transactions:
            return None
        
        return {
            "status_code": 200,
            "transactions": [
                {
                    "transaction_reference": transaction.id,
                    "payer_account": transaction.payer_account,
                    "payee_account": transaction.payee_account,
                    "amount": str(transaction.amount),
                    "currency": transaction.currency,
                    "status": transaction.status.value,
                    "created_at": transaction.created_at.isoformat(),
                    "updated_at": transaction.updated_at.isoformat(),
                    "error_message": transaction.error_message
                } for transaction in transactions
            ]
        }
    except Exception as e:
        return {
            "status_code": 500,
            "message": f"Internal server error: {str(e)}"
        }

