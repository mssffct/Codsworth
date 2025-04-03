import enum

from uuid import uuid4

from typing import Optional
from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy import UUID, DateTime, Enum
from sqlalchemy.orm import mapped_column, Mapped

from users.models import UserModel
from database import Base


class StatusEnum(enum.Enum):
    """Statuses enum"""

    actual = "actual"
    done = "done"
    expired = "expired"
    to_delete = "to_delete"


class NoteModel(Base):
    __tablename__ = "note"

    unique_id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid4)
    user: Mapped["UserModel"] = mapped_column(ForeignKey("user_account.unique_id"))
    title: Mapped[str] = mapped_column(String(256))
    content: Mapped[Optional[str]] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    status: Mapped[str] = mapped_column(
        Enum(StatusEnum), default=StatusEnum.actual, nullable=False
    )

    def __repr__(self) -> str:
        return f"Note <<{self.title}>> status <<{self.status}>> owned by {self.user.id}"
