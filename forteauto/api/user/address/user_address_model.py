from typing import Optional
import ormar
from database import document
from api.user import user_model


class Address(document.Model):

    class Meta(document.BaseMeta):
        tablename = "address"

    city: str = ormar.String(max_length=20)
    address: str = ormar.String(max_length=255)
    state: str = ormar.String(max_length=20, default="lagos")
    nearest_bus_stop: str = ormar.String(max_length=30)
    owner: Optional[user_model.User] = ormar.ForeignKey(user_model.User)
