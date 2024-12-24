from pydantic import BaseModel


class Note(BaseModel):
    id: int
    name: str