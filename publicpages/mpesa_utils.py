import requests
import base64
from datetime import datetime
from django.conf import settings

def get_mpesa_access_token():
    """Returns M-Pesa Access Token (Using Provided Credentials)"""
    return settings.MPESA_ACCESS_TOKEN  # Using the provided static token

def stk_push(phone, amount):
    """Initiates M-Pesa STK Push"""
    access_token = get_mpesa_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Generate dynamic timestamp
    password = settings.MPESA_PASSKEY  # Use provided password directly

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Donation Payment",
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()
