from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine

from litestar import Litestar
from pydantic import BaseModel as _BaseModel
from litestar.params import Parameter
from litestar.plugins.sqlalchemy import filters
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import DB_URI



@asynccontextmanager
async def db_connection(app: Litestar) -> AsyncGenerator[None, None]:
    engine = getattr(app.state, "engine", None)
    if engine is None:
        engine = create_async_engine(DB_URI)
        app.state.engine = engine
    try:
        yield
    finally:
        await engine.dispose()


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""
    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}


async def provide_limit_offset_pagination(
    current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False,
    ),
) -> filters.LimitOffset:
    """Add offset/limit pagination.

    Return type consumed by `Repository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    current_page : int
        LIMIT to apply to select.
    page_size : int
        OFFSET to apply to select.
    """
    return filters.LimitOffset(page_size, page_size * (current_page - 1))


# Dependency Provider for the session
async def provide_db_session() -> Session:
    """Dependency provider that returns a SQLAlchemy session."""
    engine = create_engine(DB_URI)
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = local_session()
    try:
        yield db
    finally:
        db.close()