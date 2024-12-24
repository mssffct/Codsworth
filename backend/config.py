import os

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
