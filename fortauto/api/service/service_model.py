from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from fortauto.database.document import BaseMeta, Model, ormar
from fortauto.api.user.property.user_property_model import Car
from fortauto.api.user.user_model import User
from fortauto.api.service.listing.service_listing_model import Service_type
from fortauto.utils.shortcuts import random_str


class Service_status(str, Enum):
    picked = "picked"
    repairing = "repairing"
    ready = "ready"
    delivered = "deliver"
    processing = "processing"


class Service_priority(str, Enum):
    quick = "quick"
    others = "others"
    standard = "standard"


service_id = random_str(size=30)


class Service(Model):

    class Meta(BaseMeta):
        pass

    owner: Optional[User] = ormar.ForeignKey(User)
    serviceId: str = ormar.String(max_length=30, default=service_id, index=True)
    car_type: Optional[Car] = ormar.ForeignKey(Car)
    service_type: Optional[Service_type] = ormar.ForeignKey(Service_type)
    additional_notes: str = ormar.Text(default="No note", nullable=True)
    quantity: int = ormar.Integer(
        maximum=300, minimum=1, nullable=True, default=1)
    status: str = ormar.String(
        max_length=20, default="processing", choices=list(Service_status))
    return_data: Optional[datetime] = ormar.DateTime(
        timezone=True, default=(datetime.utcnow() + timedelta(days=5)))
    created_at: datetime = ormar.DateTime(
        timezone=True, default=datetime.utcnow)
