from database import BaseModel
from pydantic import EmailStr, SecretStr


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


class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr
