import bcrypt
from flask import make_response, redirect, render_template, request

from init import app, db
from modelos import Usuario


def usuario_logado() -> bool:
    """
    Retorna True se o login for válido.
    Apenas funciona em contexto de uma rota.
    """
    email = request.cookies.get('login_email')
    senha = request.cookies.get('login_senha')

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

    email, senha = request.args.get('email'), request.args.get('senha')

    if ('' in (email, senha)) or (None in (email, senha)):
        return render_template('login.html', erro='Valores não podem estar vazios.')

    usuario: Usuario = Usuario.query.filter_by(email=email).first()    

    if usuario is None:
        return render_template('login.html', erro='Este usuário não existe')
    
    if not bcrypt.checkpw(bytes(senha, 'utf-8'), usuario.pwhash):
        return render_template('login.html', erro='Senha incorreta')

    resposta = make_response(redirect('/inicio'))
    resposta.set_cookie('login_email', email)
    # TODO: Ao invés de usar a senha talvez seja melhor usar um token real que ninguem vai se importar mas eu nao tenho mais nada para fazer
    resposta.set_cookie('login_senha', senha)

    return resposta

def rota_registro():
    """
    Rota para registro de um novo usuário, recebe email e senha.
    Tanto login como registro utilizam a página login.html.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if usuario_logado():
        return redirect('/inicio')

    email, senha = request.args.get('email'), request.args.get('senha')

    if ('' in (email, senha)) or (None in (email, senha)):
        return render_template('login.html', erro='Valores não podem estar vazios.')

    usuario: Usuario = Usuario.query.filter_by(email=email).first()    

    if usuario is not None:
        return render_template('login.html', erro='Este usuário já existe')

    pwhash = bcrypt.hashpw(bytes(senha, 'utf-8'), bcrypt.gensalt())

    novo_usuario = Usuario(email=email, pwhash=pwhash)
    db.session.add(novo_usuario)
    db.session.commit()

    resposta = make_response(redirect('/inicio'))
    resposta.set_cookie('login_email', email)
    resposta.set_cookie('login_senha', senha)

    return resposta

@app.route('/logout')
def logout():
    resposta = make_response(redirect('/inicio'))
    resposta.delete_cookie('login_email')
    resposta.delete_cookie('login_senha')

    return resposta