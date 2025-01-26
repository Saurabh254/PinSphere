from pydantic import BaseModel, SecretStr

from pin_sphere.users.schemas import UserCreate


class LoginUser(BaseModel):
    username: str
    password: SecretStr


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class SignupUser(UserCreate):
    pass
