from hashlib import new
import re

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt, get_current_user
from init import app, bcrypt, db, jwt, TOKEN_UPDATE_HEADER
from modelos import Usuario
from datetime import datetime, timedelta

from rotas.utils import invalid_response, valid_response, validate_data


emailPattern = re.compile(
    "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

@app.route('/api/auth/login', methods=['POST'])
def rota_login():
	'''
	Rota de login de usuário.
	Realiza a validação dos dados obtidos por formulário:
	email e senha.

	Returns:
		OK (cod. 200): objeto JSON contendo resposta de 
			feedback - senha incorreta, usuário inválido ou
			informações válidas.
	'''
	dados = validate_data(request.get_json(), {
		'email': str,
		'password': str,
	})

	usuario: Usuario = Usuario.query.filter_by(email=dados['email']).first()

	if usuario == None:
		return invalid_response('no-such-user')

	else:
		token = create_access_token(identity=usuario)
		
		response = valid_response(usuario.json()) 
		response.headers.set(TOKEN_UPDATE_HEADER, token)

		return response


@app.route('/api/auth/register', methods=['POST'])
def rota_registro():
	'''
	Rota de registro de usuário.
	Realiza a validação dos dados obtidos por formulário:
	nome, email e senha.

	Returns:
		OK (cod. 200): objeto JSON contendo resposta de 
			feedback - email inválido, usuário já existe ou
			informações válidas.
	'''
	data = validate_data(request.get_json(), {
		'name': str,
		'email': str,
		'password': str,
	})

	if Usuario.query.filter_by(email=data['email']).first() != None:
		return invalid_response('already-exists')

	elif not emailPattern.fullmatch(data['email']):
		return invalid_response('invalid-email')

	else:
		pwhash = bcrypt.generate_password_hash(data['password']) \
			.decode('utf-8', 'ignore')
		
		new_user = Usuario(
			nome=data['name'],
			email=data['email'],
			pwhash=pwhash,
		)

		token = create_access_token(identity=new_user)

		response = valid_response(new_user.json())
		response.headers.set(TOKEN_UPDATE_HEADER, token)

		return response


@app.route('/api/auth/user', methods=['GET'])
@jwt_required()
def rota_usuario():
	'''
	Rota informações usuário.
	
	Returns:
		OK (cod. 200): objeto JSON.
	'''
	return jsonify(current_user.json())


# https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading/
# Usuários são identificados por id

@jwt.user_identity_loader
def get_user_identity(user: Usuario):
    return user.id

@jwt.user_lookup_loader
def load_user(_jwt_header, jwt_data):
    return Usuario.query.get(jwt_data['sub'])

# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
# Como não utilizamos cookies, apenas é enviado o novo JWT nos headers

@app.after_request
def refresh_jwt(response: Response):
    try:
        timestamp: float = get_jwt()['exp']
        min_exp_time = datetime.timestamp(datetime.utcnow() + timedelta(minutes=15))

        if min_exp_time > timestamp:
            new_token = create_access_token(identity=get_current_user())
            response.headers.set(TOKEN_UPDATE_HEADER, new_token)

        return response
    except (RuntimeError, KeyError):
        return response


# TODO: atualizar isso aq feio
@app.route("/api/alterar-senha", methods=["POST"])
@jwt_required()
def rota_api_alterar_senha():
	'''
	Rota de alteração de senha.
	Realiza a validação dos dados obtidos por formulário:
	senha e nova senha.

	Returns:
		OK (cod. 200): objeto JSON contendo resposta de 
			feedback - senha incorreta ou
			informações válidas.
	'''
	err = None
	data = validate_data(request.get_json(), {
		'password': str,
		'newPassword': str,
	})

	if not bcrypt.check_password_hash(current_user.pwhash, data['password']):
		err = "Senha incorreta"
	else:
		nova_pwhash = bcrypt.generate_password_hash(data['newPassword']) \
			.decode('utf-8', 'ignore')

		current_user.pwhash = nova_pwhash
		db.session.commit()

	return {
		'ok': err == None,
		'erro': err,
		'errtarget': "senha", # só temos erros aqui, então...
	}