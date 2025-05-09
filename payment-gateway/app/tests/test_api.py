import pytest
from fastapi import status
from app.models.schema import PaymentRequest

@pytest.mark.asyncio
async def test_initiate_payment(client, db_session):
    payment_data = {
        "payer": "1234567890",
        "payee": "0987654321",
        "amount": 100.50,
        "currency": "USD"
    }
    
    response = client.post("/api/v1/payments", json=payment_data)
    
    assert response.status_code in [100, 200, 400]
    assert "transaction_reference" in response.json()
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_get_payment_status(client, db_session):
    # First create a payment
    payment_data = {
        "payer": "1234567890",
        "payee": "0987654321",
        "amount": 100.50,
        "currency": "USD"
    }
    create_response = client.post("/api/v1/payments", json=payment_data)
    
    # Then check its status
    transaction_id = create_response.json()["transaction_reference"]
    status_response = client.get(f"/api/v1/payments/{transaction_id}")
    
    assert status_response.status_code in [100, 200, 400]
    assert status_response.json()["transaction_reference"] == transaction_id

@pytest.mark.asyncio
async def test_invalid_payment_request(client):
    invalid_data = [
        {"payer": "123", "payee": "0987654321", "amount": 100, "currency": "USD"},  # Payer too short
        {"payer": "1234567890", "payee": "09876", "amount": 100, "currency": "USD"},  # Payee too short
        {"payer": "1234567890", "payee": "0987654321", "amount": -100, "currency": "USD"},  # Negative amount
        {"payer": "1234567890", "payee": "0987654321", "amount": 100, "currency": "US"},  # Currency too short
    ]
    
    for data in invalid_data:
        response = client.post("/api/v1/payments", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_nonexistent_transaction(client):
    response = client.get("/api/v1/payments/nonexistent-id")
    assert response.status_code == status.HTTP_404_NOT_FOUND