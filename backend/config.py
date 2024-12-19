import os

from dotenv import load_dotenv

from starlette.config import Config
from starlette.datastructures import Secret

load_dotenv()

config = Config(".env")

INSIDE_DOCKER = os.getenv("INSIDE_DOCKER")

API_PORT = config("API_PORT", cast=int, default="8000")
API_HOST = config("API_HOST", cast=str, default="127.0.0.1")
DATABASE_HOST =  "127.0.0.1" if not INSIDE_DOCKER else config("DATABASE_HOST", cast=str)
DATABASE_PORT = config("POSTGRES_PORT", cast=int)
DATABASE_PASS = config("POSTGRES_PASSWORD", cast=Secret)
DATABASE_USER = config("POSTGRES_USER", cast=Secret)
DATABASE_DB = config("POSTGRES_DB", cast=str)
