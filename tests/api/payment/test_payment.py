import warnings
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from forteauto.api.payment.payment_schema import PaymentInput, ValidatePaymet_Input, RefundInput

@pytest.fixture
@pytest.mark.asyncio
async def create_payment(authorize_client:TestClient, new_user_servce:dict):
   payment_details =PaymentInput(serviceId=new_user_servce["serviceId"], cardno="5531886652142950", cvv="564", expirymonth="09", expiryyear="32", pin="3310")
   with authorize_client as client:
           charge = client.post("payments/", json=payment_details.dict())
           assert  charge.status_code == status.HTTP_201_CREATED
           assert charge.json()["otp"] == None
           assert charge.json()["completed"] == False
           assert charge.json()["txRef"] == new_user_servce["serviceId"]
           assert charge.json()["flwRef"] !=None
           assert charge.json()["payment_Id"]  == new_user_servce["serviceId"]
           return charge.json()


@pytest.fixture
@pytest.mark.asyncio
async def validate_payment(authorize_client:TestClient, create_payment ):
   payment_details = ValidatePaymet_Input(txRef=create_payment["txRef"], flwRef=create_payment["flwRef"], otp="12345", payment_Id=create_payment["payment_Id"])
   with authorize_client as client:
           validate = client.post("payments/validate", json=payment_details.dict())
           assert validate.json() == {'message': 'Payment was successful'}
           assert validate.status_code == status.HTTP_200_OK
           return create_payment

@pytest.fixture
@pytest.mark.asyncio
async def verify_payment(authorize_client:TestClient, validate_payment ):
   with authorize_client as client:
           verify = client.get(f"payments/verify/{validate_payment['txRef']}")
           assert verify.json() == {'message': 'Payment was successful'}
           assert verify.status_code == status.HTTP_200_OK
           return validate_payment
           

@pytest.mark.asyncio
async def test_create_failed_payment(authorize_client:TestClient, new_user_servce:dict):
   payment_details =PaymentInput(serviceId=new_user_servce["serviceId"], cardno="5143010522339965", cvv="276", expirymonth="08", expiryyear="32", pin="3310")
   with authorize_client as client:
           charge = client.post("payments/", json=payment_details.dict())
           assert  charge.status_code == status.HTTP_400_BAD_REQUEST
           assert charge.json() == {"detail":"Invalid card i formation was provided"}




@pytest.mark.asyncio
async def test_refund_payment(authorize_client:TestClient, validate_payment ):
   with authorize_client as client:
           refund_input = RefundInput(txRef=validate_payment["txRef"], amount=20)
           
           res = client.post("payments/refund", json=refund_input.dict())
           if res.status_code == status.HTTP_400_BAD_REQUEST:
                warnings.warn("If you are trying this with testing card it might not work", SyntaxWarning)
                assert res.json() == {'detail': 'Error refunding, Your refund call failed with message: unauthorized'}
           else:
                assert res.status_code == status.HTTP_200_OK
           
@pytest.mark.asyncio
async def test_get_payment(authorize_client:TestClient, verify_payment ):
   with authorize_client as client:
           res = client.get(f"payments/{verify_payment['txRef']}")
           assert res.status_code == status.HTTP_200_OK
           assert res.json()["flwRef"] == verify_payment["flwRef"]
           assert res.json()["txRef"] == verify_payment["txRef"]

@pytest.mark.asyncio
async def test_all_payment(authorize_client:TestClient, verify_payment ):
   with authorize_client as client:
           res = client.get(f"payments/")
           assert res.status_code == status.HTTP_200_OK
           assert isinstance(res.json(), list)
           assert res.json()[0]["flwRef"] == verify_payment["flwRef"]
           assert res.json()[0]["txRef"] == verify_payment["txRef"]


@pytest.mark.asyncio
async def test_delete_payment(authorize_client:TestClient, verify_payment ):
   with authorize_client as client:
           res = client.delete(f"payments/{verify_payment['txRef']}")
           assert res.status_code == status.HTTP_204_NO_CONTENT
          



        
           
           
