from pydantic import BaseModel


class Vault(BaseModel):
    id: int
    name: str
