from pydantic import BaseModel, Field
from typing import Optional

class PaymentRequest(BaseModel):
    payer: str = Field(..., min_length=10, max_length=10, pattern="^[0-9]+$")
    payee: str = Field(..., min_length=10, max_length=10, pattern="^[0-9]+$")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    payer_reference: Optional[str] = None

class PaymentResponse(BaseModel):
    status_code: int
    transaction_reference: str
    message: str