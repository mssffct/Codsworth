from typing import TYPE_CHECKING


from litestar import Controller, Request, get
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from pydantic import TypeAdapter

from .instances import User
from .models import provide_users_repo, UserRepository
from litestar.plugins.sqlalchemy import filters


class UsersController(Controller):
    path = "/users"
    dependencies = {"authors_repo": Provide(provide_users_repo)}

    @get("/me")
    async def me(self, request: Request) -> User:
        return User(id=1, name="test_user")

    @get(path="/")
    async def list_users(
        self,
        authors_repo: "UserRepository",
        limit_offset: 'filters.LimitOffset',
    ) -> OffsetPagination[User]:
        """List authors."""
        results, total = await authors_repo.list_and_count(limit_offset)
        type_adapter = TypeAdapter(list[User])
        return OffsetPagination[User](
            items=type_adapter.validate_python(results),
            total=total,
            limit=limit_offset.limit,
            offset=limit_offset.offset,
        )
