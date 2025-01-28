from sqlalchemy.dialects.postgresql import UUID
from database import BaseModel


class User(BaseModel):
    id: UUID | None
    name: str
    fullname: str | None
