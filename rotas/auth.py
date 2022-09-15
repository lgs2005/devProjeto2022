import re

from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, jwt_required, current_user, get_jwt, get_current_user
from init import app, bcrypt, db, jwt, TOKEN_UPDATE_HEADER
from modelos import Usuario
from datetime import datetime, timedelta

from rotas.utils import response_err, response_ok, validar_objeto

emailPattern = re.compile(
    "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

@app.route('/api/auth/login', methods=['POST'])
def rota_login():
    dados = validar_objeto(request.get_json(), {
        'email': str,
        'password': str,
    })

    usuario: Usuario = Usuario.query.filter_by(email=dados['email']).first()

    if usuario == None:
        return response_err('no-such-user')

    elif not bcrypt.check_password_hash(usuario.pwhash, dados['password']):
        return response_err('wrong-password')

    else:
        token = create_access_token(identity=usuario)
        
        response = response_ok(usuario.json()) 
        response.headers.set(TOKEN_UPDATE_HEADER, token)

        return response


@app.route('/api/auth/register', methods=['POST'])
def rota_registro():
    dados = validar_objeto(request.get_json(), {
        'name': str,
        'email': str,
        'password': str,
    })

    if Usuario.query.filter_by(email=dados['email']).first() != None:
        return response_err('already-exists')

    elif not emailPattern.fullmatch(dados['email']):
        return response_err('invalid-email')

    else:
        pwhash = bcrypt.generate_password_hash(dados['password']) \
            .decode('utf-8', 'ignore')
        
        usuario = Usuario(
            nome=dados['name'],
            email=dados['email'],
            pwhash=pwhash,
        )

        db.session.add(usuario)
        db.session.commit()

        token = create_access_token(identity=usuario)

        response = response_ok(usuario.json())
        response.headers.set(TOKEN_UPDATE_HEADER, token)

        return response


@app.route('/api/auth/user', methods=['GET'])
@jwt_required()
def rota_usuario():
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
    erro = None
    dados = validar_objeto(request.get_json(), {
        'senha': str,
        'novaSenha': str,
    })

    if not bcrypt.check_password_hash(current_user.pwhash, dados['senha']):
        erro = "Senha incorreta"
    else:
        nova_pwhash = bcrypt.generate_password_hash(dados['novaSenha']) \
            .decode('utf-8', 'ignore')

        current_user.pwhash = nova_pwhash
        db.session.commit()

    return {
        'ok': erro == None,
        'erro': erro,
        'errtarget': "senha", # só temos erros aqui, então...
    }