import asyncio
import datetime

from typing import TypeVar, ParamSpec, Callable
from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncSession
from inspect import signature
from functools import wraps

from config import AppState

T = TypeVar("T")
P = ParamSpec("P")


def atomic(
    db_session_key: str = "session",
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        async def wrapped_func(*args: P.args, **kwargs: P.kwargs) -> T:
            db_session: AsyncSession = kwargs.get(db_session_key, None)  # type: ignore[assignment]
            try:
                result: T = await func(*args, **kwargs)
                await db_session.commit()
                return result
            except Exception as e:
                await db_session.rollback()
                raise e

        wrapped_func.__signature__ = signature(func)  # type: ignore[attr-defined]
        return wrapped_func

    return decorator


async def run_periodic_cleanup(app: Litestar) -> None:
    """Запускает задачу cleanup_database с заданным интервалом."""
    while True:
      async with app.state.db_session_maker() as db_session:  # Create a new session for each run
          app_state: AppState = app.state  # type: ignore
          app_state = AppState(interval=600, to_keep=datetime.timedelta(days=7))
          await cleanup_database(db_session, app_state)
          await asyncio.sleep(app_state.interval)


async def cleanup_database(db_session: AsyncSession, app_state: AppState):
    print(db_session, app_state)


def create_trash_collector(app: Litestar) -> None:
    app.add_background_task(run_periodic_cleanup(app))
