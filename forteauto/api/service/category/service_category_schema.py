from pydantic import BaseModel


class ServiceCategoryInput(BaseModel):
    name: str


class ServiceCategoryOutput(ServiceCategoryInput):
    id: str
