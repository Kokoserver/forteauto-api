import os
from functools import lru_cache
from typing import Union
import pydantic
from fortauto.utils import shortcuts


class Settings(pydantic.BaseSettings):
    environment:str = os.getenv("ENVIRONMENT")
    debug: bool = os.getenv("DEBUG")
    frontend_url: str = "https://www.fortauto.com"
    secret_key: str = os.getenv("SECRET_KEY")
    refresh_key: str = os.getenv("refresh_key")
    website_name: str = "forte automobile"
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    api_prefix_url:str = "/api/v1"
    api_version: Union[int, float] = os.getenv("API_VERSION")
    refresh_token_expire_time: int = os.getenv("REFRESH_TOKEN_EXPIRE_TIME")
    access_token_expire_time: int = os.getenv("ACCESS_TOKEN_EXPIRE_TIME")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")
    api_url: str = os.getenv("API_URL")
    database_url: str = os.getenv("DATABASE_URL")
    base_dir: pydantic.DirectoryPath = shortcuts.get_base_dir()
    # locate template folder at the root of the project
    template_folder: pydantic.DirectoryPath = f"{base_dir}/templates"

    # FLUTTERWAVE KEYS
    rave_public_key: str = os.getenv("RAVE_PUBLIC_KEY")
    rave_secret_key: str = os.getenv("RAVE_SECRET_KEY")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
