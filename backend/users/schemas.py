from sqlalchemy.dialects.postgresql import UUID
from database import BaseModel
from pydantic import EmailStr, SecretStr


class User(BaseModel):
    name: str
    email: EmailStr


class RegistrationSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr


class UserLoginPayload(BaseModel):
    email: EmailStr
    password: SecretStr
