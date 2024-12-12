import uvicorn

from routes import routes
from errors import *

from contextlib import asynccontextmanager
from starlette.applications import Starlette

exception_handlers = {
    404: not_found,
    500: server_error
}

@asynccontextmanager
async def lifespan(app):
    print('Startup')
    yield
    print('Shutdown')

app = Starlette(
    debug=True, routes=routes, lifespan=lifespan, exception_handlers=exception_handlers
)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)