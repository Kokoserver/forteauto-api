from decimal import Decimal
from database.document import Model, ormar, BaseMeta
from datetime import datetime


class Service_type(Model):

    class Meta(BaseMeta):
        pass

    name: str = ormar.String(max_length=300, index=True)
    description: str = ormar.Text(nullable=False)
    price: Decimal = ormar.Decimal(
        default=0, index=True, max_digits=10, decimal_places=3)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
