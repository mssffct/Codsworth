from datetime import datetime
from typing import Optional, Union
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from litestar.plugins.sqlalchemy import base, repository
from argon2 import PasswordHasher, Type as ArgonType
from argon2.exceptions import VerificationError
from sqlalchemy.ext.asyncio import AsyncSession


class UserModel(base.UUIDBase):
    __tablename__ = "user_account"  #  type: ignore[assignment]

    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    def set_password(self, value: Union[str, bytes]) -> None:
        if isinstance(value, str):
            value = value.encode()
        self.password = PasswordHasher(type=ArgonType.ID).hash(value)

    def check_password(self, value):
        ph = PasswordHasher()  # Type is implicit in hash
        try:
            ph.verify(self.password, value)
            return True
        except VerificationError:
            return False


class UserRepository(repository.SQLAlchemyAsyncRepository[UserModel]):
    """User repository."""

    model_type = UserModel


async def provide_users_repo(db_session: "AsyncSession") -> UserRepository:
    """This provides the default Authors repository."""
    return UserRepository(session=db_session)
