from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from typing import cast
from litestar import Litestar
from pydantic import BaseModel as _BaseModel
from litestar.params import Parameter
from litestar.plugins.sqlalchemy import filters

from config import DATABASE_HOST, DATABASE_PORT, DATABASE_PASS, DATABASE_USER, DATABASE_DB


DB_URI = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

def get_db_connection(app: Litestar) -> AsyncEngine:
    """Returns the db engine.

    If it doesn't exist, creates it and saves it in on the application state object
    """
    if not getattr(app.state, "engine", None):
        app.state.engine = create_async_engine(DB_URI)
    return cast("AsyncEngine", app.state.engine)


async def close_db_connection(app: Litestar) -> None:
    """Closes the db connection stored in the application State object."""
    if getattr(app.state, "engine", None):
        await cast("AsyncEngine", app.state.engine).dispose()


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
