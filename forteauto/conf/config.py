from pathlib import Path
from functools import lru_cache
from typing import Union
import pydantic
from forteauto.utils import shortcuts


class Settings(pydantic.BaseSettings):
    environment: str
    debug: bool
    frontend_url: str
    secret_key: str
    refresh_key: str
    website_name: str
    api_prefix: str
    api_version: Union[int, float]
    refresh_token_expire_time: int
    access_token_expire_time: int
    jwt_algorithm: str
    database_url: str
    base_dir: pydantic.DirectoryPath = shortcuts.get_base_dir()
    # locate template folder at the root of the project
    template_folder: pydantic.DirectoryPath = Path.joinpath(
        base_dir, "templates")

    # FLUTTERWAVE KEYS
    rave_public_key: str
    rave_secret_key: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
