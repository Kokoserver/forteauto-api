from typing import Union
from fastapi import HTTPException, status
from rave_python import Rave, RaveExceptions, Misc
from conf import config as base_config
from core.payment import rave_payment_schema as rpm


class MakePayent(object):

    def __init__(self) -> None:
        self.rave: Rave = Rave(
            publicKey=base_config.settings.rave_public_key,
            secretKey=base_config.settings.rave_secret_key,
            usingEnv=False,
            production=self.__rave_production_check())


    def __rave_production_check(self):
        return False if base_config.settings.debug else True

    def make_payment(self, card_details: rpm.Payment_card_input,
                     user: rpm.User_details_input, amount: Union[int, str]):
        try:
            self.payload = rpm.Payment_card_payloads(
                **card_details.dict(), **user.dict(), amount=amount).dict()

            self.payload["txRef"] = card_details.serviceId
            response = self.rave.Card.charge(self.payload)
            if response["suggestedAuth"]:
                auth_type: str = Misc.getTypeOfArgsRequired(
                    response["suggestedAuth"])
                if auth_type.lower() == "pin":
                    Misc.updatePayload(
                        response["suggestedAuth"],
                        self.payload,
                        pin=card_details.pin)
                    response = self.rave.Card.charge(self.payload)

                elif auth_type.lower() == "address":
                    if user.address:
                        Misc.updatePayload(
                            response["suggestedAuth"],
                            self.payload,
                            address=user.address)
                        response = self.rave.Card.charge(self.payload)
            response_data = rpm.Payment_card_charge_output(**response)
            if response_data.validationRequired:
                return rpm.Validated_Payment_card_output(
                    **response_data.dict(),
                    method=auth_type,
                    completed=False,
                    payment_Id=card_details.serviceId)
            return rpm.Validated_Payment_card_output(
                **response_data.dict(),
                completed=True,
                method=auth_type,
                payment_Id=card_details.serviceId)
        except RaveExceptions.CardChargeError as e:
            error_response = rpm.ErrorResponse(**e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response.dict())

    def validate_payment(self, val_data: rpm.Payment_validation_input):
        try:
            validation_data = rpm.Payment_validation_input(**val_data.dict())
            response = self.rave.Card.validate(
                flwRef=validation_data.flwRef, otp=validation_data.otp)
            response_data = rpm.Payment_validation_output(
                **response, completed=True, payment_Id=val_data.payment_Id)
            if not response_data.error:
                return response_data

        except RaveExceptions.TransactionValidationError as e:
            response_body = e.err["errMsg"]
            if isinstance(e.err, str):
                response_body = e.err["errMsg"]
            elif isinstance(e, dict):
                response_body = rpm.ErrorResponse(**e.err).dict()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=response_body)

    def verify(self, txRef: str):
        try:
            response = self.rave.Card.verify(txRef)
            return rpm.Payment_verification_ouput(**response, payment_Id=txRef)
        except RaveExceptions.TransactionVerificationError as e:
            response_body = e.err["errMsg"]
            if isinstance(e.err, str):
                response_body = e.err["errMsg"]
            elif isinstance(e, dict):
                response_body = rpm.ErrorResponse(**e.err).dict()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=response_body)

    def refund(self, flwRef:str, amount:float):
        try:
            response = self.rave.Card.refund(flwRef,amount)
            refund_data = rpm.Payment_Refund_output(**response)
            return refund_data
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error refunding, {e}")
