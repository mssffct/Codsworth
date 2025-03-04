from typing import Any, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel
from database import get_session_from_connection

if TYPE_CHECKING:
    from litestar.connection import ASGIConnection
    from litestar.security.jwt import Token


async def get_user(session: AsyncSession, email) -> UserModel | None:
    query = select(UserModel).where(UserModel.email == email)
    result = await session.execute(query)
    return result.scalar()


async def get_user_from_token(
    token: "Token", connection: "ASGIConnection[Any, Any, Any, Any]"
) -> UserModel | None:
    session = get_session_from_connection(connection)
    query = select(UserModel).filter(UserModel.unique_id == token.sub)
    result = await session.execute(query)
    return result.scalar()
