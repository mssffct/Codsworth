import os
import sys

from dotenv import load_dotenv

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
    'class': "picologging.handlers.FileHandler",
    "formater": "verbose",
    'mode': 'a',
    'maxBytes': 32 * 1024 * 1024,
    'backupCount': 3,
    'encoding': 'utf-8'
}

def logging_config() -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
            "verbose": {"format": '%(levelname)s %(asctime)s %(module)s %(func_name)s %(lineno)d %(message)s'}
        },
        "handlers": {
            "errorsLogHandler": {
                "level": "ERROR",
                'class': "picologging.handlers.FileHandler",
                "formater": "verbose",
                "filename": LOGDIR + '/' + ERRORFILE,
                'mode': 'a',
                'maxBytes': 32 * 1024 * 1024,
                'backupCount': 3,
                'encoding': 'utf-8'
            },
            "usersLogHandler": {
                "filename": LOGDIR + '/' + USERSFILE,
                **STANDARD_LOG_CONFIG
            },
            "notesLogHandler": {
                "filename": LOGDIR + '/' + NOTESFILE,
                **STANDARD_LOG_CONFIG
            },
            "eventsLogHandler": {
                **STANDARD_LOG_CONFIG,
                "filename": EVENTSFILE,
            },
            "vaultsLogHandler": {
                "filename": LOGDIR + '/' + VAULTSFILE,
                **STANDARD_LOG_CONFIG
            },
        },
        "loggers": {
            "errorsLog": {
                "handlers": ["errorsLogHandler"],
                "level": "ERROR",
                "propagate": False
            },
            "usersLog": {
                "handlers": ["usersLogHandler"],
                "level": "INFO",
                "propagate": False
            },
            "notesLog": {
                "handlers": ["notesLogHandler"],
                "level": "INFO",
                "propagate": False
            },
            "eventsLog": {
                "handlers": ["eventsLogHandler"],
                "level": "INFO",
                "propagate": False
            },
            "vaultsLog": {
                "handlers": ["vaultsLogHandler"],
                "level": "INFO",
                "propagate": False
            }
        },
        "log_exceptions": "always",
    }
