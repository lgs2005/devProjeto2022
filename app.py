from datetime import datetime, timedelta
from init import app, db, jwt
from flask import send_from_directory
from flask_jwt_extended import get_jwt, create_access_token, set_access_cookies, get_current_user

import modelos

import rotas.conteudo
import rotas.listar_paginas
import rotas.usuario

# https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading/

@jwt.user_identity_loader
def get_user_identity(user: modelos.Usuario):
    return user.id

@jwt.user_lookup_loader
def load_user(_jwt_header, jwt_data):
    return modelos.Usuario.query.get(jwt_data['sub'])

# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/

@app.after_request
def refresh_jwt(response):
	'''
	Redefine JWT caso o tempo de expiração esteja excedido.
	'''
	try:
		timestamp: float = get_jwt()['exp']
		min_exp_time = datetime.timestamp(datetime.utcnow() + timedelta(minutes=15))

		if min_exp_time > timestamp:
			new_token = create_access_token(identity=get_current_user())
			set_access_cookies(response, new_token)

		return response
	except (RuntimeError, KeyError):
		return response

@app.route('/', methods=['GET'])
def rota_react():
	'''
	Rota compartilhada com ReactJS.

	./static/index.html
	'''
	return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    db.create_all()
