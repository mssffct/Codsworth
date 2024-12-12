from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def not_found(request: Request, exc: HTTPException):
    """
    Return an HTTP 404.
    """
    return JSONResponse({}, status_code=404)


async def server_error(request: Request, exc: HTTPException):
    """
    Return an HTTP 500.
    """
    return JSONResponse({}, status_code=500)