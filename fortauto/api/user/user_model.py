from enum import Enum
from datetime import datetime
import pydantic
import ormar
from fortauto.core import password
from fortauto.database import document


class UserRole(str, Enum):
    admin = "admin"
    super_admin = "super_admin"
    default = "normal"


class User(document.Model):

    class Meta(document.BaseMeta):
        tablename = "users"

    first_name: str = ormar.String(max_length=20)
    last_name: str = ormar.String(max_length=20)
    email: pydantic.EmailStr = ormar.String(max_length=40)
    phone_number: str = ormar.String(max_length=15)
    password: bytes = ormar.String(max_length=100)
    is_active: bool = ormar.Boolean(default=False)
    role: str = ormar.String(
        max_length=20, choice=list(UserRole), default=UserRole.default)
    created_at: datetime = ormar.DateTime(
        default=datetime.utcnow, timezone=True)

    @ormar.property_field
    def active(self):
        return self.is_active

    @ormar.property_field
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def check_password(self, plain_password):
        check_password = password.Hasher.check_password(
            plaintext_password=plain_password, hashed_password=self.password)
        if check_password:
            return True
        return False

    def hash_password(self):
        self.password: bytes = password.Hasher.hash_password(self.password)
