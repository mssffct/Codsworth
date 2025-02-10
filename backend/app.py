import uvicorn
import sys

from config import API_PORT, API_HOST, codsworth_openapi_config
from exceptions_handlers import *

from events.routers import events_router
from notes.routers import notes_router
from users.routers import users_router
from vaults.routers import vaults_router
from database import (
    db_connection,
    provide_db_session,
    provide_limit_offset_pagination,
)

from litestar import Litestar
from litestar.di import Provide
from litestar.exceptions import ValidationException, NotFoundException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.middleware.base import DefineMiddleware

from security.authentication_middleware import JWTAuthenticationMiddleware

auth_mw = DefineMiddleware(JWTAuthenticationMiddleware, exclude=["schema", "register"])

app = Litestar(
    lifespan=[db_connection],
    route_handlers=[events_router, notes_router, vaults_router, users_router],
    exception_handlers={
        ValidationException: validation_exception_handler,
        NotFoundException: not_found_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
    middleware=[auth_mw],
    openapi_config=codsworth_openapi_config,
    dependencies={
        "limit_offset": Provide(provide_limit_offset_pagination),
        "db_session": Provide(provide_db_session),
    },
)


if __name__ == "__main__":
    assert sys.argv[-1] in ("run", "schema"), "Usage: example.py [run|schema]"

    if sys.argv[-1] == "run":
        uvicorn.run("app:app", host=API_HOST, port=int(API_PORT), reload=True)
    elif sys.argv[-1] == "schema":
        print("generating schema")
