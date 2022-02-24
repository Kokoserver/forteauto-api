from datetime import datetime
from textwrap import indent
from fortauto.database.document import Model, ormar, BaseMeta


class ServiceCategory(Model):

    class Meta(BaseMeta):
        pass

    name: str = ormar.String(max_length=300)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
