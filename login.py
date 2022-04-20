import bcrypt
from flask import make_response, redirect, render_template, request, session

from init import app, db
from modelos import Usuario


COOKIE_EMAIL = 'login_email'
COOKIE_SENHA = 'login_senha'

def usuario_logado() -> bool:
    """
    Retorna True se o login for válido.
    Apenas funciona em contexto de uma rota.
    """
    email = request.cookies.get(COOKIE_EMAIL)
    senha = request.cookies.get(COOKIE_SENHA)

    #usuario = db.session.query(Usuario).filter_by(email=email).first()
    usuario: Usuario = Usuario.query.filter_by(email=email).first()

    return usuario != None and bcrypt.checkpw(bytes(senha, 'utf-8'), usuario.pwhash)

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

    email, senha = request.args.get('email'), request.args.get('senha')
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

            novo_usuario = Usuario(email=email, pwhash=pwhash)
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