import re
import pydantic
from typing import List, Optional
from api.user.address import user_address_schema

import pydantic


class Base_types(pydantic.BaseModel):
    email: pydantic.EmailStr


class UserRegisterInput(Base_types):
    first_name: str
    last_name: str
    phone_number: str
    password: bytes = pydantic.Field(min_length=5)

    @pydantic.validator('phone_number')
    def pin_must_be_int(cls, v):
        pattern = re.compile("(^[0]\d{10}$)|(^[\+]?[234]\d{12}$)")
        if not pattern.match(v):
            raise ValueError('Please enter a valid phone number')
        return v


class GetPasswordResetLink(Base_types):
    pass
    # website_url: str


class PasswordResetInput(pydantic.BaseModel):
    token: str
    password: bytes
    confirm_password: bytes


class UserLoginInput(pydantic.BaseModel):
    username: pydantic.EmailStr
    password: bytes


class UserDataOut(Base_types):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    addresss: Optional[List[user_address_schema.AddressDetailsResponse]]


class UserAccountVerifyToken(pydantic.BaseModel):
    token: str
