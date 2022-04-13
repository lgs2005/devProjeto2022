from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask("nome")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
