from typing import Optional
from pydantic import BaseModel, condecimal


class Service_typeInput(BaseModel):
    name: str
    description: str
    price: Optional[condecimal(decimal_places=3, max_digits=10)]


class Service_typeOutput(Service_typeInput):
    id: int
