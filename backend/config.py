import os
import logging

from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import StoplightRenderPlugin


load_dotenv()

INSIDE_DOCKER = os.getenv("INSIDE_DOCKER")

API_PORT = os.getenv("API_PORT") or "8000"
API_HOST = os.getenv("API_HOST") or "127.0.0.1"

DATABASE_HOST =  "127.0.0.1" if not INSIDE_DOCKER else os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("POSTGRES_PORT")
DATABASE_PASS = os.getenv("POSTGRES_PASSWORD")
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_DB = os.getenv("POSTGRES_DB")

##
# OPENAPI
##
codsworth_openapi_config = OpenAPIConfig(
    title="Codsworth",
    description="Codsworth API",
    version="0.0.1",
    render_plugins=[StoplightRenderPlugin(
        version="7.7.18", path="/elements"
    )]
)

##
# LOGGING
##
LOGDIR = os.path.join(os.getcwd(), 'log')
ERRORFILE = 'errors.log'
USERSFILE = 'users.log'
NOTESFILE = 'notes.log'
EVENTSFILE = 'events.log'
VAULTSFILE = 'vaults.log'

STANDARD_LOG_CONFIG = {
    "level": "INFO",
    'class': "logging.handlers.RotatingFileHandler",
    "formatter": "verbose",

}

FILEHANDLER_CONFIG = {
    # 'mode': 'a',
    'maxBytes': 32 * 1024 * 1024,
    'backupCount': 3,
    'encoding': 'utf-8'
}

FORMATTERS={
    "default": {
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    },
    "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    "verbose": logging.Formatter('%(levelname)s %(asctime)s %(module)s %(func_name)s %(lineno)d %(message)s')
}

LOG_LEVELS = {
    "errorsLog": logging.ERROR,
    "eventsLog": logging.INFO,
    "notesLog": logging.INFO,
}

LOG_HANDLERS = {
    "errorsLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + '/' + ERRORFILE,
    },
    "usersLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + '/' + USERSFILE,
    },
    "notesLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + '/' + NOTESFILE,
    },
    "eventsLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + '/' + EVENTSFILE,
    },
    "vaultsLog": {
        **FILEHANDLER_CONFIG,
        "filename": LOGDIR + '/' + VAULTSFILE,
    }
}


def get_logger(mod_name: str) -> logging.Logger:
    """Return logger object."""
    logger = logging.getLogger(mod_name)
    handler = RotatingFileHandler(**LOG_HANDLERS.get(mod_name))
    handler.setFormatter(FORMATTERS.get("verbose"))
    handler.setLevel(LOG_LEVELS.get(mod_name))
    logger.addHandler(handler)
    return logger
