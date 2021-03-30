from sqlalchemy import create_engine

from chore.config import PostgresConfig
from chore.database import DataBase

engine = create_engine(PostgresConfig.uri)


def init_db():
    database = DataBase(connection=engine)
    return database


def make_stable_connection():
    database = init_db()
    session = database.make_session()
    return session
