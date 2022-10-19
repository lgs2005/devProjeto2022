from http.client import UNAUTHORIZED
import re

from flask import request, jsonify, Response, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_current_user
from init import app, bcrypt, db, jwt, TOKEN_UPDATE_HEADER
from modelos import Usuario
from datetime import datetime, timedelta

from rotas.utils import get_json_fields, reserr, resok, validar_dados

emailPattern = re.compile(
    "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")


@app.post('/api/auth/login')
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
    email, senha = get_json_fields(str, 'email', 'password')
    usuario = Usuario.query.filter_by(email=email).first()

    if usuario == None:
        return reserr('no-such-user')

    if not bcrypt.check_password_hash(usuario.hash_senha, senha):
        return reserr('wrong-password')

    token = create_access_token(identity=usuario.id)

    resposta = resok(usuario.dados())
    resposta.headers.set(TOKEN_UPDATE_HEADER, token)

    return resposta


@app.post('/api/auth/register')
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
    name, email, password = get_json_fields(str, 'name', 'email', 'password')

    if Usuario.query.filter_by(email=email).first() != None:
        return reserr('already-exists')

    if not emailPattern.fullmatch(email):
        return reserr('invalid-email')

    senha_hash = bcrypt.generate_password_hash(password).decode('UTF-8')

    usuario = Usuario()
    usuario.nome = name
    usuario.email = email
    usuario.hash_senha = senha_hash

    db.session.add(usuario)
    db.session.commit()

    token = create_access_token(identity=usuario.id)

    response = resok(usuario.dados())
    response.headers.set(TOKEN_UPDATE_HEADER, token)

    return response


@app.get('/api/auth/user')
@jwt_required()
def rota_usuario():
    '''Retorno as informações do usuário'''
    usuario: Usuario = get_current_user()
    return jsonify(usuario.dados())


# https://flask-jwt-extended.readthedocs.io/en/stable/automatic_user_loading/
# Usuários são identificados por id

@jwt.user_lookup_loader
def load_user(_jwt_header, jwt_data):
    return Usuario.query.get(jwt_data['sub'])

# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/
# Como não utilizamos cookies, apenas é enviado o novo JWT nos headers


@app.after_request
def refresh_jwt(response: Response):
    try:
        timestamp: float = get_jwt()['exp']
        min_exp_time = datetime.timestamp(
            datetime.utcnow() + timedelta(minutes=15))

        if min_exp_time > timestamp:
            new_token = create_access_token(identity=get_current_user().id)
            response.headers.set(TOKEN_UPDATE_HEADER, new_token)

        return response
    except (RuntimeError, KeyError):
        return response


# TODO: seria necessário testar a senha novamente? acho que sim.
@app.route("/api/auth/alterar-senha", methods=["POST"])
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
    usuario: Usuario = get_current_user()
    old_password, new_password = get_json_fields(str, 'old_password', 'new_password')

    if not bcrypt.check_password_hash(usuario.hash_senha, old_password):
        abort(UNAUTHORIZED)
    
    usuario.hash_senha = bcrypt.generate_password_hash(new_password).decode('UTF-8')

    db.session.commit()

    return jsonify(usuario.dados())
