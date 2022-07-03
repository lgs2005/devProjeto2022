import flask_sqlalchemy

class Model(flask_sqlalchemy.Model):
	query: flask_sqlalchemy.BaseQuery

class SQLAlchemy():
	Query = flask_sqlalchemy.BaseQuery
	Model = Model