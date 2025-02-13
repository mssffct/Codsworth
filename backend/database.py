from pydantic import BaseModel as _BaseModel
from litestar.params import Parameter
from litestar.plugins.sqlalchemy import filters, base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URI


class BaseModel(_BaseModel):
    """Extend Pydantic's BaseModel to enable ORM mode"""

    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}


Base = declarative_base()


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


engine = create_async_engine(DB_URI)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency Provider for the session
async def provide_db_session():
    """Dependency provider that returns a SQLAlchemy async session."""
    async with async_session_maker() as session:
        yield session
