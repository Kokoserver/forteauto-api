from decimal import Decimal
from enum import Enum
from datetime import datetime
from typing import Optional
import ormar
from forteauto.api.user import user_model
from forteauto.database import document
from forteauto.api.service import service_model
from forteauto.utils import shortcuts


class Payment_status(str, Enum):
    success = "success"
    pending = "pending"
    cancelled = "cancelled"
    failed = "failed"


class Payment_method(str, Enum):
    card = "card"
    wallet = "wallet",


class Payment(document.Model):

    class Meta(document.BaseMeta):
        pass

    service: Optional[service_model.Service] = ormar.ForeignKey(
        service_model.Service, unique=True)
    owner: Optional[user_model.User] = ormar.ForeignKey(user_model.User)
    status: str = ormar.String(
        max_length=20,
        choices=list(Payment_status),
        default=Payment_status.pending)
    flwRef: Optional[str] = ormar.String(
        max_length=120, default=shortcuts.random_str(15), index=True)
    txRef: str = ormar.String(
        max_length=120, default=shortcuts.random_str(15), index=True)
    total_amount: Decimal = ormar.Decimal(max_digits=10, decimal_places=3)
    created_at: datetime = ormar.DateTime(
        timezone=True, default=datetime.utcnow)


class Deposit(document.Model):

    class Meta(document.BaseMeta):
        pass

    owner: Optional[user_model.User] = ormar.ForeignKey(user_model.User)
    total_amount: Decimal = ormar.Decimal(
        max_digits=5, decimal_places=3, default=0, nullable=False)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
