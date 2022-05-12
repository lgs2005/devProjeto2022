from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import os

from SECRET_KEY import SECRET_KEY

thisFilePath = os.path.dirname(os.path.abspath(__file__))
databasePath = os.path.join(thisFilePath, 'test.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(databasePath)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
login_manager.login_message = u'Por favor, entre na sua conta para acessar esta página.'
login_manager.login_view = '.usuario/rotas_usuario.rota_login'