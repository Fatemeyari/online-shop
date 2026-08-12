import requests
import json
from django.conf import settings

class ZarinPalSandBox:

    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://127.0.0.1:8000/payment/verify/"

    def __init__(self , merchant_id=settings.MERCHANT_ID):
        self.merchant_id = merchant_id


    def payment_request(self, amount, description="پرداختی کاربر"):
        payload={
            "merchant_id": self.merchant_id,
            "amount": str(amount),
            "callback_url":self._callback_url,
            "description":description,
            }
        
        headers={
            "Content-Type":"application/json"
            }

        response = requests.post(
            self._payment_request_url , headers=headers , data=json.dumps(payload)
            )
        return response.json()
    
    def payment_verify(self, amount , authority):
        payload={
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority":authority,
            }

        headers={
            "Content-Type":"application/json"
            }

        response = requests.post(
            self._payment_verify_url , headers=headers , data=json.dumps(payload)
            )
        return response.json()
    

    def generate_payment_url(self,authority):
        return f"{self._payment_page_url}{authority}"


 

if __name__ == "__main__":
    zarinpal = ZarinPalSandBox("1344b5d4-0048-11e8-94db-005056a205be")
    response = zarinpal.payment_request("15000")
    print(response)

    input("proceed to generating payment url\n")
    print(zarinpal.generate_payment_url(response["data"]["authority"]))

    input("\ncheck the payment")
    response = zarinpal.payment_verify(15000 , response["data"]["authority"])
    print(response)
