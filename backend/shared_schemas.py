from pydantic import BaseModel
from pydantic import UUID4
from typing import Optional


class CreateSuccess(BaseModel):
    unique_id: UUID4
    message: Optional[str]
