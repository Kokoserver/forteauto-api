import pydantic


class _Base_type(pydantic.BaseModel):
    refresh_token: str


class TokenData(_Base_type):
    access_token: str
    token_type: str = "bearer"


class UserRefreshTokenInput(_Base_type):
    pass


class UpdateUserInput(pydantic.BaseModel):
    userId: str

class ToEncode(pydantic.BaseModel):
    id:int
    role:str
    is_active:bool