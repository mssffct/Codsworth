from pydantic import BaseModel


# TODO explore cons & pros of msgspec usage instead of pydantic
class Note(BaseModel):
    id: int
    name: str