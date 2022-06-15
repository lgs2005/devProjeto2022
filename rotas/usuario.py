import re
from flask import request, redirect, render_template, jsonify
from flask_login import current_user, login_user, logout_user

from modelos import Usuario
from init import bcrypt, db
from rotas.utils import validar_objeto


emailPattern = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

def rota_login():
    """
    Template utilizado: 'login.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """

    if current_user.is_authenticated:
        return redirect("/inicio")
    else:
        return render_template("login.html")


def rota_api_login():
    """
    Rota para login e regitro de usuários.
    Para login, recebe email e senha.
    Para registro, recebe também o nome.

    Foi feita uma separação entre erros que o usuário pode cometer; o
    JavaScript ficou responsável por aqueles erros mais "genéricos":
        -> Email vazio;
        -> Senha vazia;
        -> Nome de usuário vazio;
        -> Email inválido (com base em um padrão web).
    
    O Python (back-end) ficou responsável por informações que só podem
    ser validadas após o envio do formulário:
        -> Usuário já existe (email já cadastrado no banco de dados);

    Caso o usuário já estiver logado, mas enviar informações de login válidas,
    sua sessão será sobrescrita.
    """

    dados = validar_objeto(request.get_json(), {
        'email': str,
        'senha': str,
    })

    sucesso = False
    usuario_final = None
    erro = None

    # se não for especificado, é False
    if not dados.get('registro', False):
        usuario: Usuario = Usuario.query.filter_by(email=dados['email']).first()

        if usuario == None:
            erro = "Este usuário não existe."
        elif not bcrypt.check_password_hash(usuario.pwhash, dados['senha']):
            erro = "Senha incorreta."
        else:
            sucesso = True
            usuario_final = usuario
    else:
        # se for um registro, precisamos validar informações extras
        dados = validar_objeto(dados, {
            'nome': str,
        })
        
        if Usuario.query.filter_by(email=dados['email']).first() != None:
            erro = "Este usuário já existe."
        elif (not emailPattern.fullmatch(dados['email'])):
            erro = "Email inválido."
        else:
            pwhash = bcrypt.generate_password_hash(dados['senha']) \
                .decode('utf-8', 'ignore')
                
            novo_usuario = Usuario(
                nome=dados['nome'],
                email=dados['email'],
                pwhash=pwhash,
            )

            db.session.add(novo_usuario)
            db.session.commit()

            sucesso = True
            usuario_final = novo_usuario
    
    if sucesso and usuario_final != None:
        if current_user.is_authenticated:
            logout_user()
        login_user(usuario_final)
    
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
            'methods': ["GET"],
            'view_func': rota_login,
        },

        '/api/login': {
            'methods': ["POST"],
            'view_func': rota_api_login
        },

        '/logout': {
            'methods': ["GET", "POST"],
            'view_func': rota_logout,
        },
    }