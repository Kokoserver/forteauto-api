import ormar
from fortauto.database import database_dependencies as db_deps


class BaseMeta(ormar.ModelMeta):
    metadata = db_deps.metadata
    database = db_deps.database


class Model(ormar.Model):

    class Meta(BaseMeta):
        abstract = True
    id: int = ormar.Integer(primary_key=True, index=True, nullable=True)
