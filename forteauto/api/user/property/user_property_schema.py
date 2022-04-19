from typing import Optional
import pydantic


class _Base_type(pydantic.BaseModel):
    maker: str 
    model: str


class Base_Car_details(_Base_type):
    maker: Optional[str]
    model: Optional[str]
    vin_number: Optional[str] = pydantic.Field(min_length=13)


class Car_details_Optional(Base_Car_details):
    pass


class CarDetail(_Base_type):
        vin_number:str = pydantic.Field(min_length=13)


class CarDetailResponse(CarDetail):
    id: int
