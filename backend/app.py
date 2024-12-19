import uvicorn

from routes import routes
from errors import *
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
    uvicorn.run(app, host=API_HOST, port=API_PORT)