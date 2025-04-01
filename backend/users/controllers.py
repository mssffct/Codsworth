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
from sqlalchemy.exc import IntegrityError

from .schemas import UserLogin, RegistrationSchema, UserInfo
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
            user = UserModel(email=data.email, name=data.name)
            user.set_password(data.password.get_secret_value())
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
            return {
                "message": "User registered successfully",
                "user_id": user.unique_id,
                "redirect": "/users/login",
            }
        except IntegrityError:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"User with {data.email} already exists!",
            )
        except Exception as e:
            await db_session.rollback()
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

    @post("/login")
    async def login(self, data: UserLogin, db_session: AsyncSession) -> Redirect:
        """Authorize user"""
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

    @get("/me")
    async def me(self, request: Request) -> UserInfo:
        user: UserModel | None = request.user
        if not user:
            raise NotAuthorizedException()
        return UserInfo(email=user.email, name=user.name)

    @get("/logout")
    async def logout(self, request: Request) -> Redirect:
        """Delete jwt cookie and redirects"""
        response = Redirect(path="/users/me", status_code=HTTP_302_FOUND)
        response.delete_cookie(COOKIE_NAME, domain=COOKIE_DOMAIN)
        return response
