from pydantic import BaseModel
from pydantic import UUID4
from enum import Enum
from typing import Optional


class CreateSuccess(BaseModel):
    unique_id: UUID4
    message: Optional[str]


class Status(str, Enum):
    actual = "actual"
    done = "done"
    expired = "expired"
    to_delete = "to_delete"