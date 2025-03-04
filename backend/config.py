import os
import logging

from datetime import timedelta
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import StoplightRenderPlugin


load_dotenv()

INSIDE_DOCKER = os.getenv("INSIDE_DOCKER")

API_PORT = os.getenv("API_PORT") or "8000"
API_HOST = os.getenv("API_HOST") or "127.0.0.1"

DATABASE_HOST = "127.0.0.1" if not INSIDE_DOCKER else os.getenv("DB_HOST")
DATABASE_PORT = os.getenv("DB_PORT")
DATABASE_PASS = os.getenv("DB_PASSWORD")
DATABASE_USER = os.getenv("DB_USER")
DATABASE_DB = os.getenv("DB_NAME")

DB_URI = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

##
# Authentication
##
JWT_SECRET = os.getenv("JWT_SECRET")
AUTH_HEADER = "X_Auth_Token"
COOKIE_NAME = "token"
COOKIE_DOMAIN = None
COOKIE_SECURE = False  # TODO set to True under https
COOKIE_HTTP_ONLY = True
COOKIE_SAMESITE = "lax"
COOKIE_EXPIRE = timedelta(minutes=24 * 60)  # 1 day

##
# OPENAPI
##
codsworth_openapi_config = OpenAPIConfig(
    title="Codsworth",
    description="Codsworth API",
    version="0.0.1",
    render_plugins=[StoplightRenderPlugin(version="7.7.18", path="/")],
)

##
# LOGGING
##
LOGDIR = os.path.join(os.getcwd(), "log")
ERRORFILE = "errors.log"
USERSFILE = "users.log"
NOTESFILE = "notes.log"
EVENTSFILE = "events.log"
VAULTSFILE = "vaults.log"


FILEHANDLER_CONFIG = {
    "mode": "a",
    "maxBytes": 32 * 1024 * 1024,
    "backupCount": 3,
    "encoding": "utf-8",
}

FORMATTERS = {
    "standard": "%(levelname)s [%(asctime)s] - %(message)s",
    "verbose": "%(levelname)s [%(asctime)s] :: %(module)s F: [%(funcName)s %(lineno)d] M: [%(message)s]",
}

LOG_HANDLERS = {
    "errorsLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + ERRORFILE,
    },
    "usersLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + USERSFILE,
    },
    "notesLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + NOTESFILE,
    },
    "eventsLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + EVENTSFILE,
    },
    "vaultsLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + "/" + VAULTSFILE,
    },
}

LOGGING_DATE_FMT = "%d-%m-%Y %H:%M:%S"


def get_logger(
    mod_name: str, level: str = logging.INFO, formatter: str = "standard"
) -> logging.Logger:
    """
    Args:
        mod_name: module name
        level: logging level
        formatter: string key in FORMATTERS dict ("standard", "verbose", etc.)
    Returns:
        logging.Logger
    """
    handler = RotatingFileHandler(**LOG_HANDLERS.get(mod_name))
    fmt = FORMATTERS.get(formatter)
    handler.setFormatter(logging.Formatter(fmt, LOGGING_DATE_FMT))

    logger = logging.getLogger(mod_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
