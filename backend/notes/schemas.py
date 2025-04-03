from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import UUID4

from .models import StatusEnum

# TODO explore cons & pros of msgspec usage instead of pydantic


class Status(str, Enum):
    actual = "actual"
    done = "done"
    expired = "expired"
    to_delete = "to_delete"


class Note(BaseModel):
    unique_id: UUID4
    title: str
    content: Optional[str]
    created_at: datetime
    status: StatusEnum


class NoteCreate(BaseModel):
    title: str
    content: Optional[str]