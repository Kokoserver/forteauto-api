from typing import Optional
from datetime import datetime
import pydantic

# base requirement


class Base_types(pydantic.BaseModel):
    txRef: Optional[str]
    flwRef: Optional[str]


class Base_txRef(pydantic.BaseModel):
    txRef: Optional[str]


class Base_flwRef(pydantic.BaseModel):
    flwRef: Optional[str]


class Base_status(pydantic.BaseModel):
    completed: Optional[bool] = False


# base required card details


class Card_details_base(pydantic.BaseModel):
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


# all card required input


class Payment_card_input(Card_details_base):
    serviceId: str
    pin: str = pydantic.Field(
        title="card pin",
        description="Customer card pin",
        min_length=4,
        max_length=4)


# contains both card details and user information as requirement by payment gateway


class Payment_card_payloads(Card_details_base):
    email: pydantic.EmailStr
    phonenumber: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]
    amount: int
    Ip: Optional[str]


# payment reponse to pydantic from payment gateway


class Payment_card_charge_output(Base_types):
    validationRequired: Optional[bool] = False
    suggestedAuth: Optional[bytes]
    authUrl: Optional[str]
    error: bool = False


# payment  validation input (required is txRef, and note both txRef and payent_id are the same)


class Payment_validation_output(Base_status):
    payment_Id: str
    status: str
    message: str
    error: bool


# payment validation required input None: required input are (otp, flwRef)
class Validate_payment_data_types(Base_flwRef):
    payment_Id: Optional[str]
    otp: Optional[str]


# Valdated payment card response from payment gateway to pydantic
class Validated_Payment_card_output(Validate_payment_data_types, Base_txRef,
                                    Base_status):
    method: str = "card"


# payment validation input inherite Validate_payment_data_types to avaoid duplications


class Payment_validation_input(Validate_payment_data_types):
    pass


class User_address(pydantic.BaseModel):
    city: Optional[str]
    state: Optional[str]
    country: Optional[str] = pydantic.Field(max_length="2", default="NG")
    zipcode: Optional[str] = "100001"  # lagos zip code


# user input only payment gateway only required user email


class User_details_input(pydantic.BaseModel):
    phonenumber: Optional[str]
    email: pydantic.EmailStr
    firstname: Optional[str]
    lastname: Optional[str]
    # embeded dict of User_address, for card that is not from Nigerian banks
    address: Optional[User_address]
    Ip: Optional[str]


# payment verication input required only txRef from payment gateway,
#  which is the same thing as paymentId or payment_Id


class Payment_verification_input(Base_txRef):
    pass


# all the payment verifaction on success output converted to pydantic


class Payment_verification_ouput(Base_types, Base_status):
    status: str = "success"
    payment_Id: Optional[str]
    chargedamount: Optional[int]
    vbvmessage: Optional[str]
    error: Optional[bool] = False
    cardToken: Optional[str]
    chargemessage: Optional[str]
    acctmessage: Optional[str]
    currency: str
    chargecode: str
    amount: Optional[int]
    transactionComplete: bool = False
    meta: Optional[list]


# payment  refund input both pydantic.fields are required, by payment gateway
class Payemt_refund_input(Base_flwRef):
    amount: int


# payment refund meta data i.e addtional information of the account to be refunded
class Payment_refund_meta_data(pydantic.BaseModel):
    source: str
    disburse_ref: str
    disburse_status: str


# all the payment refund on success output converted to pydantic
class Payment_Refund_output(Base_status):
    settlement_id: str
    id: int
    AccountId: int
    TransactionId: int
    FlwRef: str
    walletId: int
    AmountRefunded: str
    status: str
    destination: str
    meta: Optional[Payment_refund_meta_data]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


# error response cocverted to pydantic
class ErrorResponse(Base_types):
    error: bool = False
    errMsg: Optional[str]
