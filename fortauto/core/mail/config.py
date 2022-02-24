import os
from functools import lru_cache
import pydantic


def get_base_dir():
    current_wdr = os.getcwd()
    if os.path.isdir(os.path.join(current_wdr, os.getcwd().split("\\")[-1])):
        return os.path.join(current_wdr, os.getcwd().split("\\")[-1])
    return os.getcwd()


class Settings(pydantic.BaseSettings):
    default_website_url: str = "https://www.kokoserver.com"
    email_server: str = os.getenv("EMAIL_SERVER", 'smtp.gmail.com')
    email_server_port: int = os.getenv("EMAIL_SERVER_PORT", 587)
    admin_email: pydantic.EmailStr = os.getenv("ADMIN_EMAIL")
    admin_password: str = os.getenv("ADMIN_PASSWORD")
    website_name: str = os.getenv("WEBSITE_NAME", "kokoserver")
    base_dir: pydantic.DirectoryPath = get_base_dir()
    # locate template folder at the root of the project
    template_folder: pydantic.DirectoryPath = f"{base_dir}/templates"

    class Config:
        env_file = "./.env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
