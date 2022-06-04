from http.client import BAD_REQUEST
import re
from flask import request, redirect, render_template, abort, jsonify
from flask_login import current_user, login_user, logout_user

from modelos import Usuario
from init import bcrypt, db


emailPattern = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

def rota_login():
    """
    Rota para login do usuário, recebe nome, email e senha.

    Foi feita uma separação entre erros que o usuário pode cometer; o
    JavaScript ficou responsável por aqueles erros mais "genéricos":
        -> Email vazio;
        -> Senha vazia;
        -> Email inválido (com base em um padrão web).
    
    O Python (back-end) ficou responsável por informações que só podem
    ser validadas após o envio do formulário:
        -> Usuário não existe (email não está no banco de dados);
        -> Senha incorreta (usuário existe porém senha está incorreta).

    Template utilizado: 'login.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """

    if current_user.is_authenticated:
        return redirect('/inicio')

    if request.method == "GET":
        return render_template('login.html')
    
    elif request.method == "POST":
        fields: dict[str, str] = request.get_json()

        if (type(fields) != dict):
            abort(BAD_REQUEST)
        
        if (("email" not in fields) or ("senha" not in fields)):
            abort(BAD_REQUEST)

        email = fields["email"]
        senha = fields["senha"]

        sucesso: bool = False
        erro: str = "none"

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

    Foi feita uma separação entre erros que o usuário pode cometer; o
    JavaScript ficou responsável por aqueles erros mais "genéricos":
        -> Email vazio;
        -> Senha vazia;
        -> Nome de usuário vazio;
        -> Email inválido (com base em um padrão web).
    
    O Python (back-end) ficou responsável por informações que só podem
    ser validadas após o envio do formulário:
        -> Usuário já existe (email já cadastrado no banco de dados);

    Template utilizado: 'login.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if current_user.is_authenticated:
        return redirect('/inicio')

    if request.method == "GET":
        return render_template('login.html')

    elif request.method == "POST":
        fields: dict[str, str] = request.get_json()

        if (type(fields) != dict):
            abort(BAD_REQUEST)

        if (("email" not in fields) or ("senha" not in fields) or ("nome" not in fields)):
            abort(BAD_REQUEST)

        email = fields["email"]
        senha = fields["senha"]
        nome = fields["nome"]

        sucesso: bool = False
        erro = "none"
        

        if Usuario.query.filter_by(email=email).first() != None:
            erro = "Este usuário já existe."

        elif (not emailPattern.fullmatch(email)):
            erro = "Email inválido."

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