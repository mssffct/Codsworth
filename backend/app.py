import uvicorn
import sys

from advanced_alchemy.extensions.litestar import SQLAlchemyInitPlugin
from advanced_alchemy.extensions.litestar.plugins import SQLAlchemyAsyncConfig

from config import API_PORT, API_HOST, codsworth_openapi_config
from exceptions_handlers import *

from events.routers import events_router
from users.controllers import UsersController
from notes.controllers import NotesController
from vaults.routers import vaults_router
from database import (
    provide_db_session,
)
from config import DB_URI

from litestar import Litestar
from litestar.di import Provide
from litestar.exceptions import ValidationException, NotFoundException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

from security.jwt import jwt_cookie_auth


sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=DB_URI,
    session_dependency_key="session",
)

app = Litestar(
    route_handlers=[events_router, NotesController, vaults_router, UsersController],
    on_app_init=[jwt_cookie_auth.on_app_init],
    exception_handlers={
        ValidationException: validation_exception_handler,
        NotFoundException: not_found_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
    openapi_config=codsworth_openapi_config,
    dependencies={
        "db_session": Provide(provide_db_session),
    },
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
)


if __name__ == "__main__":
    assert sys.argv[-1] in ("run", "schema"), "Usage: example.py [run|schema]"

    if sys.argv[-1] == "run":
        uvicorn.run("app:app", host=API_HOST, port=int(API_PORT), reload=True)
    elif sys.argv[-1] == "schema":
        print("generating schema")
