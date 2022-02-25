from typing import Optional
import ormar
from database import document
from api.user import user_model


class Car(document.Model):

    class Meta(document.BaseMeta):
        pass

    maker: Optional[str] = ormar.String(max_length=30, default=None)
    model: Optional[str] = ormar.String(max_length=20, default=None)
    vin_number: Optional[str] = ormar.String(
        max_length=30, index=True, unique=True, default=None)
    owner: Optional[user_model.User] = ormar.ForeignKey(
        user_model.User, index=True)
