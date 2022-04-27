from typing import Union
import bcrypt
from flask import make_response, redirect, render_template, request, session

from init import app, db
from modelos import Usuario


COOKIE_EMAIL = 'login_email'
COOKIE_SENHA = 'login_senha'

def usuario_logado() -> Union[Usuario, None]:
    """
    Retorna o usuário que estpa acessando esta rota.
    Se não tiver um usuário logado, será retornado None.
    """
    email = request.cookies.get(COOKIE_EMAIL)
    senha = request.cookies.get(COOKIE_SENHA)

    if None in (email, senha): return None

    usuario: Usuario = Usuario.query.filter_by(email=email).first()
    senha_b = bytes(senha, 'utf-8')

    if usuario == None: return None
    if bcrypt.checkpw(senha_b, usuario.pwhash) == False: return None

    return Usuario

def rota_login():
    """
    Rota para login do usuário, recebe email e senha.
    Tanto login como registro utilizam a página login.html.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if usuario_logado():
        return redirect('/inicio')

    # TODO: Adicionar nome do usuário

    email = request.args.get('email')
    senha = request.args.get('senha')
    erro = None

    if None in (email, senha):
        erro = None
    elif '' in (email, senha):
        erro = 'Valores não podem estar vazios.'
    else:
        usuario: Usuario = Usuario.query.filter_by(email=email).first()

        if usuario is None:
            erro = 'Este usuário não existe.'
        elif not bcrypt.checkpw(bytes(senha, 'utf-8', usuario.pwhash)):
            erro = 'Senha Incorreta'
        else:
            resposta = make_response(redirect('/inicio'))
            resposta.set_cookie(COOKIE_EMAIL, email)
            resposta.set_cookie(COOKIE_SENHA, senha)
            return resposta

    return render_template('login.html', erro=erro)

def rota_registro():
    """
    Rota para registro de um novo usuário, recebe email e senha.
    Tanto login como registro utilizam a página login.html.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if usuario_logado():
        return redirect('/inicio')

    email = request.args.get('email')
    senha = request.args.get('senha')
    erro = None

    if None in (email, senha):
        erro = None
    elif '' in (email, senha):
        erro = 'Valores não podem estar vazios.'
    else:
        usuario: Usuario = Usuario.query.filter_by(email=email).first()

        if usuario is not None:
            erro = 'Este usuário já existe.'
        else:
            pwhash = bcrypt.hashpw(bytes(senha, 'utf-8'), bcrypt.gensalt())

            novo_usuario = Usuario(email=email, pwhash=pwhash, nome='teste')
            db.session.add(novo_usuario)
            db.session.commit()

            resposta = make_response(redirect('/inicio'))
            resposta.set_cookie(COOKIE_EMAIL, email)
            resposta.set_cookie(COOKIE_SENHA, senha)
            return resposta

    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    resposta = make_response(redirect('/inicio'))
    resposta.delete_cookie(COOKIE_EMAIL)
    resposta.delete_cookie(COOKIE_SENHA)

    return resposta