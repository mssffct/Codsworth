import uvicorn
import sys

from routes import routes
from errors import *
from openapi_schema import schemas
from config import API_PORT, API_HOST
from database import database

from contextlib import asynccontextmanager
from starlette.applications import Starlette


exception_handlers = {
    404: not_found,
    500: server_error
}

@asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

app = Starlette(
    debug=True, routes=routes,
    lifespan=lifespan, exception_handlers=exception_handlers
)


if __name__ == "__main__":
    assert sys.argv[-1] in ("run", "schema"), "Usage: example.py [run|schema]"

    if sys.argv[-1] == "run":
        uvicorn.run(app, host=API_HOST, port=API_PORT)
    elif sys.argv[-1] == "schema":
        schema = schemas.get_schema(routes=app.routes)
