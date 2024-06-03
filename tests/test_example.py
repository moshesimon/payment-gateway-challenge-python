from fastapi.testclient import TestClient
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from payment_gateway_api.app import app, marshal_aquirer_payload

client = TestClient(app)
def test_example():

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"app": "payment-gateway-api"}

def test_payment_Rejected():

    response = client.post("/payment", json={
        "card_number": "2222405343277",
        "cvv": "123",
        "expiry_month": 12,
        "expiry_year": 2023,
        "amount": 100,
        "currency": "USD"
    })

    assert response.status_code == 200
    assert response.json()['status'] == 'Rejected'

def test_payment_Declined():

    response = client.post("/payment", json={
        "card_number": "2222405343248112",
        "cvv": "456",
        "expiry_month": 1,
        "expiry_year": 2026,
        "amount": 60000,
        "currency": "USD"
    })

    assert response.status_code == 200
    assert response.json()['status'] == 'Declined'

def test_payment_Authorized():

    response = client.post("/payment", json={
        "card_number": "2222405343248877",
        "cvv": "123",
        "expiry_month": 4,
        "expiry_year": 2025,
        "amount": 100,
        "currency": "GBP"
    })

    assert response.status_code == 200
    assert response.json()['status'] == 'Authorized'

def test_marshal_aquirer_payload():
    data = {
        "card_number": "2222405343248877",
        "cvv": "123",
        "expiry_month": 4,
        "expiry_year": 2025,
        "amount": 100,
        "currency": "GBP"
    }
    assert marshal_aquirer_payload(data) == {
        "card_number": "2222405343248877",
        "expiry_date": "04/2025",
        "currency": "GBP",
        "amount": 100,
        "cvv": "123"
        }
    
def test_okay():
    response = client.post("/payment")
    print(response.json)
    assert response.status_code == 200

test_payment_Declined()
# test_payment_Authorized()

# test_payment_Rejected()
# test_marshal_aquirer_payload()
