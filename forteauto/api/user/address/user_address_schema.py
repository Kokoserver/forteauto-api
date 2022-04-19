import pydantic


class AddressDetails(pydantic.BaseModel):
    state: str
    city: str
    address: str
    nearest_bus_stop: str


class AddressDetailsResponse(AddressDetails):
    id: int
