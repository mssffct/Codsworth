from litestar.exceptions import InternalServerException, ValidationException, NotFoundException
from litestar import Litestar, MediaType, Request, Response, get


def not_found_handler(request: Request, exc: NotFoundException):
    return Response(
        media_type=MediaType.TEXT,
        content=f"not found: {exc}",
        status_code=404
    )


def internal_server_error_handler(request: Request, exc: Exception) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=f"server error: {exc}",
        status_code=500,
    )


def validation_exception_handler(request: Request, exc: ValidationException) -> Response:
    return Response(
        media_type=MediaType.TEXT,
        content=f"validation error: {exc.detail}",
        status_code=400,
    )

