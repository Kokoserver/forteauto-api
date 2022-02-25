from pydantic import BaseModel
from typing import Optional, Union
from api.service.listing.service_listing_schema import Service_typeOutput
from api.service.service_model import Service_status
from api.user.property.user_property_schema import Car_details_Optional


class service_typeInput(BaseModel):
    id: int


class ServiceBase(BaseModel):
    car_type: Car_details_Optional
    service_type: int
    additional_notes: Optional[str]
    quantity: Optional[int] = 1


class ServiceOutput(ServiceBase):
    id: int
    serviceId: str
    car_type: Union[Car_details_Optional, dict]
    service_type: Union[dict, Service_typeOutput]
    status: Service_status


class ServiceInput(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    car_type: Optional[Car_details_Optional]
    status: Service_status = Service_status.processing
