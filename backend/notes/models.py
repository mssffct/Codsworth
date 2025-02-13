import uuid

from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, Mapped

from users.models import UserModel
from database import Base


class Note(Base):
    __tablename__ = "note"

    id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    # user: Mapped["UserModel"] = mapped_column(ForeignKey("user_account"))
    title: Mapped[str] = mapped_column(String(30))
    content: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Note {self.title} owned by {self.user.id}"
