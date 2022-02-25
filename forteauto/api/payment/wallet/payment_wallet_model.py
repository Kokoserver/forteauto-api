from decimal import Decimal
from datetime import datetime
import ormar
from api.user import user_model
from database import document


class Wallet(document.Model):

    class Meta(document.BaseMeta):
        pass

    balance: Decimal = ormar.Decimal(max_digits=5, decimal_places=3, default=0)
    owner: user_model.User = ormar.ForeignKey(user_model.User)
    created_at: datetime = ormar.DateTime(
        timezone=True, default=datetime.utcnow)
