from typing import Any, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .models import UserModel
from .schemas import RegistrationSchema, RegistrationSuccess
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


async def register_user(
    session: AsyncSession, data: RegistrationSchema
) -> RegistrationSuccess | ValueError:
    try:
        user = UserModel(email=data.email, name=data.name)
        user.set_password(data.password.get_secret_value())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return RegistrationSuccess(
            message="User registered successfully",
            user_id=user.unique_id,
            redirect="/users/login",
        )
    except IntegrityError:
        raise ValueError(f"User with {data.email} already exists!")
    except Exception as e:
        await session.rollback()
        raise ValueError(str(e))
