from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from typing import cast
from litestar import Litestar

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