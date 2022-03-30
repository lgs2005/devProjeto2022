from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask('lindo sabado letivo estou aqui escrevendo isso')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
