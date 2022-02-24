from datetime import datetime
from typing import Optional
import pydantic
from fortauto.api.service.listing import service_listing_schema
from fortauto.api.user.property import user_property_schema


class PaymentInput(pydantic.BaseModel):
    serviceId: str = pydantic.Field(
        title="A unique id for the payent",
        description="this will be the unique id for the payent and is the same thing as txRef or tx_ref"
    )
    cardno: pydantic.PaymentCardNumber
    cvv: str = pydantic.Field(
        title="card cvv",
        description="Customer cvv",
        max_lenght=3,
        min_length=3)
    expirymonth: str = pydantic.Field(
        title="card expire month", description="Customer card expire month")
    expiryyear: str = pydantic.Field(
        title="card expire year", description="Customer card expire year")
    currency: Optional[str] = "NGN"
    pin: str = pydantic.Field(
        title="card pin",
        description="Customer card pin",
        min_length=4,
        max_length=4)
    schema_extra = {
        "card_example": {
        "cardno": "5531886652142950",
        "cvv": "564",
        "expiry_month": "09",
        "expiry_year": "32",
        "pin": "3310"
        }
    }

    @pydantic.validator('cvv')
    def cvv_must_be_int(cls, v):
        if not int(v):
            raise ValueError('cvv can not contains alphabet')
        return v

    @pydantic.validator('pin')
    def pin_must_be_int(cls, v):
        if not int(v):
            raise ValueError('pin can not contains alphabet')
        return v

    @pydantic.validator('expiryyear')
    def expiryyear_must_be_int(cls, v):
        if not int(v):
            raise ValueError('expiryyear can not contains alphabet')

        if not len(v) == 2:
            raise ValueError(
                f'expiry year can not be more  or less 2 character ')
        return v

    @pydantic.validator('expirymonth')
    def expirymont_must_be_int(cls, v):
        if not int(v):
            raise ValueError('expiry mounth can not contains alphabet')

        if not len(v) == 2:
            raise ValueError(
                f'expiry mounth can not be more  or less 2 character ')
        return v


class Base_types(pydantic.BaseModel):
    flwRef: str
    txRef: str


class RefundInput(pydantic.BaseModel):
    txRef: str
    amount: float


class ValidatedPaymentInput(Base_types):
    otp: str 
    schema_extra = {
        "example": {
        "otp": "12345"
        }
    }


class ValidatePaymet_Input(ValidatedPaymentInput):
    payment_Id: Optional[str]



class Payment_Update_Input(Base_types):
    status: str


class Payment_Service_Output(pydantic.BaseModel):
    serviceId: str
    car_type: user_property_schema.CarDetail
    service_type: service_listing_schema.Service_typeOutput


class Payment_Owner_Ouput(pydantic.BaseModel):
    id: int
    first_name: str
    last_name: str
    email: pydantic.EmailStr
    phone_number: str


class Payment_Output(Base_types):
    id: int
    status: str
    total_amount: int
    service: Payment_Service_Output
    owner: Payment_Owner_Ouput
    created_at: datetime
