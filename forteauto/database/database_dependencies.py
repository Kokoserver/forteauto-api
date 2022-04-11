from fastapi import FastAPI
import databases
import sqlalchemy
from forteauto.conf import config as base_config

def get_db_url():
    if base_config.settings.environment == "test" or base_config.settings.environment == "testing":
        test_db_url =  f"sqlite:///testing.sqlite"
        return test_db_url
    elif base_config.settings.environment == "production" and not base_config.settings.debug:
        database_url = f"postgresql://{base_config.settings.database_username}:{base_config.settings.database_password}@{base_config.settings.database_host}:{base_config.settings.database_port}/{base_config.settings.database_name}"
        return database_url

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
