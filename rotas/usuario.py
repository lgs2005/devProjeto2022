from http.client import OK
import re

from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, current_user, set_access_cookies, unset_jwt_cookies

from init import app, bcrypt, catimg, db
from modelos import Usuario

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

	elif not bcrypt.check_password_hash(usuario.pwhash, dados['password']):
		return invalid_response('wrong-password')

	else:
		response = valid_response(usuario.json()) 
		token = create_access_token(identity=usuario)
		set_access_cookies(response, token)
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

		db.session.add(new_user)
		db.session.commit()

		response = valid_response(new_user.json()) 
		token = create_access_token(identity=new_user)
		set_access_cookies(response, token)
		return response


@app.route('/api/auth/logout', methods=['POST'])
def rota_logout():
	'''
	Rota logout de usuário da sessão.

	Faz a retificação de valores JWT para vazios.

	Returns: 
		OK (cod. 200): logout válido.
	'''
	response = make_response(catimg(OK), OK)
	unset_jwt_cookies(response)
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