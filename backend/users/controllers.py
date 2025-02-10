from litestar import Controller, Request, get, post
from litestar.di import Provide
from litestar.pagination import OffsetPagination
from litestar.params import Body
from pydantic import TypeAdapter
from litestar.datastructures import State
from litestar.status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from litestar.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .schemas import User, RegistrationSchema
from .models import provide_users_repo, UserModel


class UsersController(Controller):
    path = "/users"
    dependencies = {"authors_repo": Provide(provide_users_repo)}

    @post("/register", status_code=HTTP_201_CREATED)
    async def register_user(self, db_session: Session, data: RegistrationSchema = Body()) -> dict | HTTPException:
        """Register new user"""
        try:
            user = UserModel(email=data.email, name=data.name)
            user.set_password(data.password.get_secret_value())
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return {"message": "User registered successfully", "user_id": user.id}
        except Exception as e:
            db_session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

    @get("/me")
    async def me(self, request: Request) -> User:
        return User(id=1, name="test_user")

    # @get(path="/")
    # async def list_users(
    #     self,
    #     authors_repo: "UserRepository",
    #     limit_offset: "filters.LimitOffset",
    # ) -> OffsetPagination[User]:
    #     """List authors."""
    #     results, total = await authors_repo.list_and_count(limit_offset)
    #     type_adapter = TypeAdapter(list[User])
    #     return OffsetPagination[User](
    #         items=type_adapter.validate_python(results),
    #         total=total,
    #         limit=limit_offset.limit,
    #         offset=limit_offset.offset,
    #     )
