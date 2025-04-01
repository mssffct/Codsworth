from config import (
    JWT_SECRET,
    COOKIE_EXPIRE,
    COOKIE_SAMESITE,
    COOKIE_SECURE,
    COOKIE_DOMAIN,
)

from users.crud import get_user_from_token
from litestar.security.jwt import JWTCookieAuth


jwt_cookie_auth = JWTCookieAuth["UserModel"](
    retrieve_user_handler=get_user_from_token,
    token_secret=JWT_SECRET,
    exclude=["/users/login", "/schema", "/users/register"],
    default_token_expiration=COOKIE_EXPIRE,
    samesite=COOKIE_SAMESITE,
    secure=COOKIE_SECURE,
    domain=COOKIE_DOMAIN,
)
