from http.client import BAD_REQUEST
import re
from flask import request, redirect, render_template, flash, abort, jsonify
from flask_login import current_user, login_user, logout_user

from modelos import Usuario
from init import bcrypt, db

emailPattern = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

# esse back-end ta meio nebuloso
# nao daria pra fazer a autenticacao do usuario na mesma rota?
# login e registrar na mesma rota

def rota_login():
    """
    Rota para login do usuário, recebe nome, email e senha.

    Template utilizado: 'login.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """

    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect('/')
        else:
            return render_template('login.html')
    
    elif request.method == "POST":
        dados: dict[str, str] = request.get_json()

        if (type(dados) != dict):
            abort(BAD_REQUEST)
        
        if (("email" not in dados) or ("senha" not in dados)):
            abort(BAD_REQUEST)

        email = dados["email"]
        senha = dados["senha"]
        sucesso = False
        erro = "none"

        # acho que não é necessário validar o email e a senha aqui
        # ja que isto já é feito durante o registro, então seria
        # impossível fazer login com email e senha inválidos de qualquer
        # jeito

        usuario: Usuario = Usuario.query.filter_by(email=email).first()

        if usuario == None:
            erro = "Este usuário não existe."
        elif not bcrypt.check_password_hash(usuario.pwhash, senha):
            erro = "Senha incorreta."
        else:
            if current_user.is_authenticated:
                logout_user()

            login_user(usuario)
            sucesso = True

        return jsonify({
            'sucesso': sucesso,
            'erro': erro,
        })


def rota_registro():
    """
    Rota para registro de um novo usuário, recebe nome, email e senha.

    Template utilizado: 'login.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if request.method == "GET":
        return redirect("/login")

    elif request.method == "POST":
        dados: dict[str, str] = request.get_json()

        if (type(dados) != dict):
            abort(BAD_REQUEST)

        # se qualquer um destes não existir, será abortado
        for campo in ["email", "senha", "nome"]:
            if campo not in dados:
                abort(BAD_REQUEST)

        email = dados["email"]
        senha = dados["senha"]
        nome = dados["nome"]
        sucesso = False
        erro = "none"

        if (not emailPattern.fullmatch(email)):
            erro = "E-mail inválido."
        elif (senha == ""):
            erro = "Senha inválida."
        else:
            if Usuario.query.filter_by(email=email).first() != None:
                erro = "Este usuário já existe."
            else:
                pwhash = bcrypt.generate_password_hash(senha) \
                    .decode('utf-8', 'ignore')
                    
                novo_usuario = Usuario(
                    nome=nome,
                    email=email,
                    pwhash=pwhash,
                )

                db.session.add(novo_usuario)
                db.session.commit()

                if current_user.is_authenticated:
                    logout_user()

                login_user(novo_usuario)
                sucesso = True
        
        return jsonify({
            'sucesso': sucesso,
            'erro': erro,
        })


def rota_logout():
    """
    Rota para logout do usuário.
    """
    logout_user()
    return redirect('/')


def adicionar_rotas():
    return {

        '/login': {
            'methods': ["POST", "GET"],
            'view_func': rota_login
        },

        '/registrar': {
            'methods': ["POST", "GET"],
            'view_func': rota_registro
        },

        '/logout': rota_logout,
    }