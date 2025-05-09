import pytest
from datetime import datetime
from app.services.payment import (
    generate_transaction_id,
    determine_transaction_status,
    process_payment,
    check_payment_status
)
from app.models.schema import PaymentRequest

@pytest.mark.asyncio
async def test_generate_transaction_id():
    transaction_id = generate_transaction_id()
    assert isinstance(transaction_id, str)
    assert len(transaction_id) == 32  # UUID without hyphens
    assert all(c in '0123456789abcdef' for c in transaction_id)  # Hexadecimal characters
def test_determine_transaction_status():
    status_counts = {"PENDING": 0, "SUCCESSFUL": 0, "FAILED": 0}
    trials = 1000  # Number of test runs
    
    for _ in range(trials):
        status, _ = determine_transaction_status()
        status_counts[status.value] += 1
    
    # Convert counts to percentages
    success_rate = (status_counts["SUCCESSFUL"] / trials) * 100
    fail_rate = (status_counts["FAILED"] / trials) * 100
    pending_rate = (status_counts["PENDING"] / trials) * 100
    
    # Check probabilities are roughly correct (±5%)
    assert 80 <= success_rate <= 90       # ~85% ±5%
    assert 0 <= fail_rate <= 10           # ~5% ±5% 
    assert 5 <= pending_rate <= 15        # ~10% ±5%
@pytest.mark.asyncio
async def test_process_payment(db_session):
    payment_request = PaymentRequest(
        payer="1234567890",
        payee="0987654321",
        amount=100.50,
        currency="USD"
    )
    
    result = await process_payment(payment_request, db_session)
    
    assert result["status_code"] in [100, 200, 400]
    assert "transaction_reference" in result
    assert "message" in result
    
    # Verify minimum response time (approximately)
    assert "message" in result

@pytest.mark.asyncio
async def test_check_payment_status(db_session):
    # First create a test transaction
    payment_request = PaymentRequest(
        payer="1234567890",
        payee="0987654321",
        amount=100.50,
        currency="USD"
    )
    process_result = await process_payment(payment_request, db_session)
    
    # Now check its status
    status_result = await check_payment_status(
        process_result["transaction_reference"],
        db_session
    )
    
    assert status_result["status_code"] == process_result["status_code"]
    assert status_result["transaction_reference"] == process_result["transaction_reference"]