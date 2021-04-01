from sqlalchemy import create_engine

from config import PostgresConfig
from database import DataBase

engine = create_engine(PostgresConfig.uri)


def init_db():
    database = DataBase(connection=engine)
    return database
