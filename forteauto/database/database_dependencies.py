from fastapi import FastAPI
import databases
import sqlalchemy
from forteauto.conf import config as base_config

database_url = f"postgresql://{base_config.settings.database_username}:{base_config.settings.database_password}@{base_config.settings.database_host}:{base_config.settings.database_port}/{base_config.settings.database_name}"

test_db_url =  f"postgresql://{base_config.settings.database_username}:{base_config.settings.database_password}@{base_config.settings.database_host}:{base_config.settings.database_port}/{base_config.settings.database_name}_test"
    

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
