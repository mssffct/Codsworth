from database import BaseModel
from pydantic import EmailStr, SecretStr, UUID4


class User(BaseModel):
    name: str
    email: EmailStr


class UserInfo(BaseModel):
    name: str
    email: str


class RegistrationSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr


class RegistrationSuccess(BaseModel):
    message: str
    user_id: UUID4
    redirect: str


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr
