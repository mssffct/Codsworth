from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse


HTML_404 = "<div>404</div>"
HTML_500 = "<div>500</div>"

async def not_found(request: Request, exc: HTTPException):
    """
    Return an HTTP 404.
    """
    return HTMLResponse(HTML_404, status_code=404)


async def server_error(request: Request, exc: HTTPException):
    """
    Return an HTTP 500.
    """
    return HTMLResponse(HTML_500, status_code=500)
