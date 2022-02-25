import asyncio
import pytest
import sqlalchemy
from forteauto.main import app
from forteauto.database import database_dependencies
from fastapi import testclient
from forteauto.conf import config as base_config




@pytest.fixture(autouse=True)
def get_db():
    engine = sqlalchemy.create_engine(f"{base_config.settings.database_url}_test")
    database_dependencies.metadata.drop_all(engine)
    database_dependencies.metadata.create_all(engine)
    yield
    database_dependencies.metadata.create_all(engine)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

@pytest.fixture(scope="session")
def client():
    client = testclient.TestClient(app=app)
    client.base_url += base_config.settings.api_prefix  # adding prefix
    client.base_url = client.base_url.rstrip("/") + "/"
    yield client



