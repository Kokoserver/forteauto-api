from fastapi import FastAPI
import databases
import sqlalchemy
from conf import config as base_config


def get_db_url():
    if base_config.settings.environment == "test" or "testing":
        return f"{base_config.settings.database_url}_test"
    return base_config.settings.database_url


database_url = get_db_url()

database = databases.Database(database_url)
metadata = sqlalchemy.MetaData(database)
engine = sqlalchemy.create_engine(database_url)

async def connect_datatase(app: FastAPI) -> None:
    metadata.create_all(engine)
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


async def disconnect_datatase(app: FastAPI) -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()