import uvicorn
import sys

from config import API_PORT, API_HOST, codsworth_openapi_config
from exceptions_handlers import *

from events.routers import events_router
from notes.routers import notes_router
from users.routers import users_router
from vaults.routers import vaults_router
from database import get_db_connection, close_db_connection

from litestar import Litestar
from litestar.exceptions import ValidationException, NotFoundException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR


app = Litestar(
    on_startup=[get_db_connection],
    on_shutdown=[close_db_connection],
    route_handlers=[events_router, notes_router, vaults_router, users_router],
    exception_handlers={
        ValidationException: validation_exception_handler,
        NotFoundException: not_found_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
    openapi_config=codsworth_openapi_config
)


if __name__ == "__main__":
    assert sys.argv[-1] in ("run", "schema"), "Usage: example.py [run|schema]"

    if sys.argv[-1] == "run":
        uvicorn.run("app:app", host=API_HOST, port=int(API_PORT), reload=True)
    elif sys.argv[-1] == "schema":
        print("generating schema")
