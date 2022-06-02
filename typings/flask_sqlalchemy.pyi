import sqlalchemy.orm

class Model():
    query: sqlalchemy.orm.Query

class SQLAlchemy():
    session: sqlalchemy.orm.Session
    Model: Model