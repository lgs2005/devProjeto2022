from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
db.create_all()
