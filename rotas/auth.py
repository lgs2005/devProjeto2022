import re
from datetime import datetime, timedelta
from http.client import BAD_REQUEST, CONFLICT, NOT_FOUND, UNAUTHORIZED
from operator import itemgetter
from os import abort

from flask import Response, jsonify, request
from flask_jwt_extended import (create_access_token, get_current_user, get_jwt,
                                jwt_required)
from init import TOKEN_UPDATE_HEADER, app, bcrypt, db, jwt
from modelos import Usuario

from rotas.utils import get_campos

emailPattern = re.compile(
    "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")


@app.post('/api/auth/login')
def rota_login():
	'''
	Rota de login de usuário.
	Realiza a validação dos dados obtidos por formulário:
	email e senha.

	Returns:
		200 OK: Os dados do usuário, com o token de acesso
		404 NOT FOUND: Este usuário não existe
		401 UNAUTHORIZED: Senha incorreta
	'''
	email, password = get_campos(str, 'email', 'password')
	usuario = Usuario.query.filter_by(email=email).first()

	if usuario == None:
		abort(NOT_FOUND)

	if not bcrypt.check_password_hash(usuario.pwhash, password):
		abort(UNAUTHORIZED)

	token = create_access_token(identity=usuario.id)
		
	response = jsonify(usuario.dados())
	response.headers.set(TOKEN_UPDATE_HEADER, token)

	return response


@app.post('/api/auth/register')
def rota_registro():
	'''
	Rota de registro de usuário.
	Realiza a validação dos dados obtidos por formulário:
	nome, email e senha.

	Returns:
		200 OK: Os dados do novo usuário, com token de acesso.
		400 BAD REQUEST: Dado fornecido não está nos padrões requeridos (email)
		409 CONFLICT: Este usuário já existe
	'''
	name, email, password = get_campos(str, 'name', 'email', 'password')

	if not emailPattern.fullmatch(email):
		abort(BAD_REQUEST)

	if Usuario.query.filter_by(email=email).first() != None:
		abort(CONFLICT)

	pwhash = bcrypt.generate_password_hash(password).decode('UTF-8')

	usuario = Usuario(
		nome=name,
		email=email,
		pwhash=pwhash,
	)

	db.session.add(usuario)
	db.session.commit()

	token = create_access_token(identity=usuario.id)

	response = jsonify(usuario.dados())
	response.headers.set(TOKEN_UPDATE_HEADER, token)

	return response


@app.get('/api/auth/user')
@jwt_required()
def rota_usuario():
	'''Rota que retorna informações do usuário logado.'''
	return jsonify(Usuario.logado.dados())


@jwt.user_lookup_loader
def load_user(jwt_header, jwt_data):
    return Usuario.query.get(jwt_data['sub'])


@app.after_request
def refresh_jwt(response: Response):
	try:
		timestamp: float = get_jwt()['exp']
		min_exp_time = datetime.timestamp(datetime.utcnow() + timedelta(minutes=15))

		if min_exp_time > timestamp:
			new_token = create_access_token(identity=get_current_user().id)
			response.headers.set(TOKEN_UPDATE_HEADER, new_token)

		return response
	except (RuntimeError, KeyError):
		return response


@app.patch('/api/auth/alter')
@jwt_required()
def rota_api_alterar_senha():
	'''
	Rota de alteração do usuário
	Returns:
		200 OK: Novos dados do usuário
		500 BAD REQUEST: Especifique a senha, ou e-mail inválido
		401 UNAUTHORIZED: Senha incorreta
		409 CONFLICT: E-mail já está em uso
	'''
	dados = request.get_json()
	password = dados['password']

	if type(password) != str or type(dados['new']) != dict:
		abort(BAD_REQUEST)

	if not bcrypt.check_password_hash(Usuario.logado.pwhash, password):
		abort(UNAUTHORIZED)

	new_email, new_name, new_password = itemgetter('email', 'name', 'password')(dados['new'])
	
	if type(new_email) == str:
		if not emailPattern.fullmatch(new_email):
			abort(BAD_REQUEST)

		if Usuario.query.filter_by(email=new_email).first() != None:
			abort(CONFLICT)

		Usuario.logado.email = new_email

	if type(new_name) == str:
		Usuario.logado.nome = new_name
	
	if type(new_password) == str:
		new_hash = bcrypt.generate_password_hash(new_password).decode('UTF-8')
		Usuario.logado.pwhash = new_hash

	db.session.commit()
	return jsonify(Usuario.logado.dados())


# {
# 	'password': 'fodase',
# 	'new': {
# 		'email': '',
# 		'name': '',
# 		'password': ''
# 	}
# }
