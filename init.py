from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask("projeto 2")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
