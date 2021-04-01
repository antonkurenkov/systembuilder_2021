class SQLiteConfig:
    name = 'db.sqlite'
    url = rf'sqlite:///{name}'


class PostgresConfig:
    name = 'postgres'
    user = 'admin'
    password = 'admin'
    host = 'db'
    port = '5432'
    uri = rf'postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'
