from sqlalchemy.orm import sessionmaker, Session

from models.base import Base, BaseModel


class DBSession:
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except Exception as error:
            print(error)

    def close_session(self):
        self._session.close()

    def commit_session(self):
        try:
            self._session.commit()
        except Exception as error:
            print(error)


class DataBase:
    session_factory: sessionmaker

    _test_query = 'SELECT 1'

    def __init__(self, connection):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def create_all_tables(self):
        Base.metadata.create_all(self.connection)

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session=session)
