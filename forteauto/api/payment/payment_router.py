from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from api.payment import payment_model
from api.payment import payment_schema
from core.authentication import UserWrite
from api.service import service_model
from api.user.address import user_address_model
from api import api_base_schema as base_schema
from core.payment import rave_payement
from core.payment import rave_payment_schema
from api.payment import payment_schema
from utils import shortcuts

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_card_payment(paymentDetails: payment_schema.PaymentInput,
                              request: Request,
                              user: int = Depends(UserWrite.current_user)):

    get_service: service_model.Service = await service_model.Service.objects.select_related(
        ["service_type",
         "owner"]).get_or_none(serviceId=paymentDetails.serviceId)
    if not get_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Serice with id:{paymentDetails.serviceId} does not exist")
    if not get_service.owner.id == user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this service does nnot belong to user with id:{user}")
    total_amount = get_service.service_type.price
    if total_amount < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="payment amount must be greater than 0, or contact the admin"
        )

    user_address: user_address_model.Address = await user_address_model.Address.objects.filter(
        owner=user).all()
    user_address = shortcuts.get_user_address(user_address=user_address)
    fortato_payment = rave_payement.MakePayent()
    user_details: rave_payment_schema.User_details_input = rave_payment_schema.User_details_input(
        email=get_service.owner.email,
        firstname=get_service.owner.first_name,
        lastname=get_service.owner.last_name,
        address=user_address,
        phonenumber=get_service.owner.phone_number,
        Ip=request.client.host)
    response = fortato_payment.make_payment(
        card_details=paymentDetails, user=user_details, amount=total_amount)
    if response.completed:
        verification_response = fortato_payment.verify(txRef=response.txRef)
        if verification_response.transactionComplete:
            new_service_payment = await payment_model.Payment(
                **response.dict(),
                status=payment_model.Payment_status.success,
                owner=user,
                service=get_service,
                total_amount=total_amount).save()
            if new_service_payment:
                await get_service.update(payment=new_service_payment)
                return base_schema.Message(message="Payment was successful")
    if not response.flwRef:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid card i formation was provided")
    return response


@router.post("/validate")
async def payment_validate(validate_data: payment_schema.ValidatePaymet_Input,
                           user: int = Depends(UserWrite.current_user)):
    get_service: service_model.Service = await service_model.Service.objects.select_related(
        "service_type").get_or_none(serviceId=validate_data.txRef)
    fortato_payment: rave_payement.MakePayent = rave_payement.MakePayent()
    response = fortato_payment.validate_payment(val_data=validate_data)
    if response.completed:
        verification_response = fortato_payment.verify(
            txRef=get_service.serviceId)
        if verification_response.transactionComplete:
            new_service_payment = await payment_model.Payment(
                owner=user,
                service=get_service.id,
                total_amount=get_service.service_type.price,
                status=payment_model.Payment_status.success,
                txRef=validate_data.payment_Id,
                flwRef=validate_data.flwRef).save()
        if new_service_payment:
            return base_schema.Message(message="Payment was successful")
    return response


@router.get("/verify/{payment_id}")
async def payment_verify(payment_id: str,
                         user: int = Depends(UserWrite.current_user)):
    get_payent = await payment_model.Payment.objects.get_or_none(
        txRef=payment_id, owner=user)
    if not get_payent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment with id:{paymentId} is not found")
    fortato_payment = rave_payement.MakePayent()
    verification_response = fortato_payment.verify(txRef=get_payent.txRef)
    if verification_response.transactionComplete:
        verify_service_payment = await get_payent.update(
            status=payment_model.Payment_status.success,
            total_amount=verification_response.amount)
        if verify_service_payment:
            return base_schema.Message(message="Payment was successful")

    return verification_response


@router.post("/refund")
async def payments_refund(refund_data: payment_schema.RefundInput,
                          user: int = Depends(UserWrite.current_user)):
    get_payent: payment_model.Payment = await payment_model.Payment.objects.get_or_none(
        txRef=refund_data.txRef, owner=user)
    if not get_payent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Payment with id:{refund_data.txRef} is not found")
    fortato_payment: rave_payement.MakePayent = rave_payement.MakePayent()
    refund_response: rave_payment_schema.Payment_Refund_output = fortato_payment.refund(
        flwRef=get_payent.flwRef, amount=refund_data.amount)
    if refund_response.completed:
        new_total_amount = (
            get_payent.total_amount - refund_response.AmountRefunded)
        verify_service_payment: payment_model.Payment = await payment_model.Payment.objects.update(
            status=payment_model.Payment_status.success,
            total_amount=new_total_amount)
        if verify_service_payment:
            return base_schema.Message(message="Payment was successful")
    return refund_response


@router.get("/{txRef}", response_model=payment_schema.Payment_Output)
async def get_single_payment(txRef: str,
                             user: int = Depends(UserWrite.current_user)):
    payment: payment_model.Payment = await payment_model.Payment.objects.select_all(
        follow=True).get_or_none(
            txRef=txRef, owner=user)
    if payment:
        return payment
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"payment with id:{txRef} does not exist")


@router.get("/", response_model=list[payment_schema.Payment_Output])
async def get_all_payment(user: int = Depends(UserWrite.current_user)):
    get_payment = await payment_model.Payment.objects.select_all(
        follow=True).filter(owner=user).all()
    if get_payment:
        return get_payment
    return []


@router.delete("/{txRef}")
async def delete_payment(txRef: str,
                         user: int = Depends(UserWrite.current_user)):
    payment: payment_model.Payment = await payment_model.Payment.objects.get_or_none(
        txRef=txRef, owner=user)
    if payment:
        await payment.delete()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="payment does not exist")
