from typing import Optional, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from litestar.plugins.sqlalchemy import base, repository
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserModel(base.UUIDBase):
    __tablename__ = "user_account"  #  type: ignore[assignment]

    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]


class UserRepository(repository.SQLAlchemyAsyncRepository[UserModel]):
    """User repository."""

    model_type = UserModel


async def provide_users_repo(db_session: "AsyncSession") -> UserRepository:
    """This provides the default Authors repository."""
    return UserRepository(session=db_session)
