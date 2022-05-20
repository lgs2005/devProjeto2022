import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

caminho_base = os.path.dirname(__file__)

app = Flask("projeto 2")

app.config['SECRET_KEY'] = b'1b86a0bc41f04a3fa76bef86ddde883b0a641dde57afa55e4dbe761cfa08c314'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho_base}/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_message = u"Por favor, entre na sua conta para acessar esta página."
login_manager.login_message_category = "info"
login_manager.login_view = 'rota_login'
