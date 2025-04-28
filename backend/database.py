from typing import TYPE_CHECKING

from advanced_alchemy.extensions.litestar.plugins import SQLAlchemyInitPlugin
from pydantic import BaseModel as _BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from advanced_alchemy.extensions.litestar.plugins import SQLAlchemyAsyncConfig
from litestar.exceptions import ImproperlyConfiguredException

from config import DB_URI

if TYPE_CHECKING:
    from litestar import Litestar
    from litestar.connection import ASGIConnection


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}


Base = declarative_base()

engine = create_async_engine(DB_URI)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency Provider for the session
async def provide_db_session():
    """Dependency provider that returns a SQLAlchemy async session."""
    async with async_session_maker() as session:
        yield session


def get_sqlalchemy_plugin(app: "Litestar") -> SQLAlchemyInitPlugin:
    """Get the SQLAlchemyPlugin from the Litestar application."""
    try:
        return app.plugins.get(SQLAlchemyInitPlugin)
    except KeyError as e:
        raise ImproperlyConfiguredException(
            "The SQLAlchemyPlugin is missing from the application"
        ) from e


def get_session_from_connection(connection: "ASGIConnection") -> AsyncSession:
    sqlalchemy_config = get_sqlalchemy_plugin(connection.app).config[0]
    if not isinstance(sqlalchemy_config, SQLAlchemyAsyncConfig):
        raise ImproperlyConfiguredException(
            "SQLAlchemy config must be of type `SQLAlchemyAsyncConfig`"
        )
    async_session = sqlalchemy_config.provide_session(
        state=connection.app.state, scope=connection.scope
    )
    return async_session
