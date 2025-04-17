from typing import TypeVar, ParamSpec, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from inspect import signature
from functools import wraps


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
