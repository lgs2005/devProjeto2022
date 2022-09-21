from datetime import timedelta
from typing import TYPE_CHECKING
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

if TYPE_CHECKING:
	import db_type_proxy
	db: db_type_proxy.SQLAlchemy

# X -> header customizado, OTP -> OnTrack Pages
TOKEN_UPDATE_HEADER = 'X-OTP-Update-Bearer-Token'

caminho_base = os.path.dirname(__file__)
app = Flask("projeto 2")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho_base}/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['JWT_SECRET_KEY'] = 'b227b977deca4b8bacfe627c35511a16-libarya-librya-lbirayry-libsty-nocap?-5b72846c1cf441ad8cc1363ede851336'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1, minutes=20)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
cors = CORS(app, expose_headers=[TOKEN_UPDATE_HEADER])
jwt = JWTManager(app)

def catimg(code):
	return f'<img src="https://http.cat/{code}"/>'
