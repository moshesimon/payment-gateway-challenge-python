from typing import Dict
from fastapi import FastAPI, HTTPException, Request, Header
import requests
import ipdb
import uuid

app = FastAPI()

def validate_request(request):
    # validate request
    return True

@app.get("/")
async def ping() -> Dict[str, str]:
    return {"app": "payment-gateway-api"}

@app.post("/payment")
async def payment(request: Request, authorization: str = Header(...)):
    # check authorization header
    # decode the token to get the merchant_id

    data = await request.json()

    # check if similar request has been made recently from the same user
    # if yes, return the previous payment record
    # else, store the payment record and proceed with the payment process

    # (don't remember what else you asked me to write comments on sorry!)
    
    if validate_request(data):
        print("Request is valid")
        
        json = marshal_aquirer_payload(data)

        response = requests.post("http://localhost:8080/payments",json=json, headers={"Content-Type": "application/json"})
        
        if response.status_code != 200: # not all error codes are 200
            raise HTTPException(status_code=400, detail="Bank generated an error")

        bank_response = response.json()
        payment_status = "Authorized" if bank_response["authorized"] else "Declined"
    else:
        payment_status = "Rejected"

    
    payment_id = str(uuid.uuid4())
    payment_record = {
        "id": payment_id,
        "card_number": data["card_number"][-4:],
        "amount": data["amount"],
        "currency": data["currency"],
        "status": payment_status,
        "expiry_month": data["expiry_month"],
        "expiry_year": data["expiry_year"],
    }
    
    # updated the payment record with the payment status

    return payment_record

def marshal_aquirer_payload(data):
    return {
        "card_number": data["card_number"],
        "cvv": data["cvv"],
        "expiry_date": f'{data["expiry_month"]:02}/{data["expiry_year"]}',
        "amount": data["amount"],
        "currency": data["currency"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)