from litestar import Router

from .controllers import UsersController


users_router = Router(path="/", route_handlers=[UsersController])
