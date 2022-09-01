from http.client import OK
import re

from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, current_user, set_access_cookies, unset_jwt_cookies
from init import app, bcrypt, catimg, db
from modelos import Usuario

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
        response = response_ok(usuario.json()) 
        token = create_access_token(identity=usuario)
        set_access_cookies(response, token)
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

        response = response_ok(usuario.json()) 
        token = create_access_token(identity=usuario)
        set_access_cookies(response, token)
        return response


@app.route('/api/auth/logout', methods=['POST'])
def rota_logout():
    response = make_response(catimg(OK), OK)
    unset_jwt_cookies(response)
    return response


@app.route('/api/auth/user', methods=['GET'])
@jwt_required()
def rota_usuario():
    return jsonify(current_user.json())


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