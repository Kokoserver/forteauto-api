import os
from pathlib import Path
from functools import lru_cache
import pydantic
from fortauto.utils import shortcuts


class Settings(pydantic.BaseSettings):
    default_website_url: str = "https://www.kokoserver.com"
    email_server: str = os.getenv("EMAIL_SERVER", 'smtp.gmail.com')
    email_server_port: int = os.getenv("EMAIL_SERVER_PORT", 587)
    admin_email: pydantic.EmailStr = os.getenv("ADMIN_EMAIL")
    admin_password: str = os.getenv("ADMIN_PASSWORD")
    website_name: str = os.getenv("WEBSITE_NAME", "kokoserver")
    base_dir: pydantic.DirectoryPath = shortcuts.get_base_dir()
    # locate template folder at the root of the project
    template_folder: pydantic.DirectoryPath = Path.joinpath(base_dir, "fortauto", "templates")


    class Config:
        env_file = "./.env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

