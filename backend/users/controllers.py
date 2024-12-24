from litestar import Controller, Request, get

from .instances import User


class UsersController(Controller):
    path = "/users"

    @get('/me')
    async def me(self, request: Request) -> User:
        return User(id=1, name="test_user")