from litestar import Controller, Request, get, post
from litestar.params import Body
from litestar.response import Redirect
from litestar.status_codes import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_302_FOUND,
)
from litestar.exceptions import HTTPException, NotAuthorizedException
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserLogin, RegistrationSchema
from .crud import get_user
from config import COOKIE_NAME, COOKIE_DOMAIN
from users.models import UserModel
from security.jwt import jwt_cookie_auth


class UsersController(Controller):
    path = "/users"

    @post("/register", status_code=HTTP_201_CREATED)
    async def register_user(
        self, db_session: AsyncSession, data: RegistrationSchema = Body()
    ) -> dict | HTTPException:
        """Register new user"""
        try:
            # TODO check unique username and email
            user = UserModel(email=data.email, name=data.name)
            user.set_password(data.password.get_secret_value())
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
            return {
                "message": "User registered successfully",
                "user_id": user.unique_id,
            }
        except Exception as e:
            await db_session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

    @post("/login")
    async def login(self, data: UserLogin, db_session: AsyncSession) -> Redirect:
        """Аутентифицирует пользователя и устанавливает JWT в Cookie."""
        user = await get_user(db_session, data.email)
        if not user or not user.check_password(data.password):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        response = jwt_cookie_auth.login(
            identifier=str(user.unique_id), send_token_as_response_body=True
        )
        return response

    @get("/protected")
    async def protected(self, request: Request) -> dict:
        """Защищенный эндпоинт, требующий аутентификации."""
        user: UserModel | None = request.user
        if not user:
            raise NotAuthorizedException()
        return {"message": f"Hello, {user.name}!", "user_id": user.unique_id}

    @get("/")
    async def home(self) -> dict:
        return {"message": "Welcome!"}

    @get("/logout")
    async def logout(self, request: Request) -> Redirect:
        """Удаляет Cookie с JWT."""
        response = Redirect(path="/users/protected", status_code=HTTP_302_FOUND)
        response.delete_cookie(COOKIE_NAME, domain=COOKIE_DOMAIN)
        return response
