import databases
import sqlalchemy

from config import DATABASE_HOST, DATABASE_PORT, DATABASE_PASS, DATABASE_USER, DATABASE_DB

metadata = sqlalchemy.MetaData()

db_url = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

database = databases.Database(db_url)