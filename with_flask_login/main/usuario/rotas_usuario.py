from flask import make_response, redirect, render_template, request
from flask_login import current_user, logout_user, login_user
from config import db, bcrypt

from modelos import Usuario

def rota_login():
    """
    Rota para login do usuário, recebe nome, email e senha.

    Tanto login quanto registro utilizam a página login.html.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if current_user.is_authenticated:
        return redirect('/inicio')

    nomeFormulario = request.args.get('nome')
    emailFormulario = request.args.get('email')
    senhaFormulario = request.args.get('senha')
    error = None

    # TODO: usuário vai receber um erro assim que entrar no site, pois o valor, quando entrar, vai ser None.
    if None  in (nomeFormulario, emailFormulario, senhaFormulario):
        error = 'Valores não podem estar vazios.'
    if '' in (nomeFormulario, emailFormulario, senhaFormulario):
        error = 'Valores não podem estar vazios.'
    else:
        usuario: Usuario = Usuario.query.filter_by(email=emailFormulario).first()

        if usuario is None:
            error = 'Este usuário não existe'
        elif not bcrypt.check_password_hash(usuario.pwhash, senhaFormulario):
            error = 'Por faver, cheque sua senha'
        else:
            login_user(usuario)
            resposta = make_response(redirect('/inicio'))
            return resposta
    return render_template('login.html', erro=error, titulo='Login')


def rota_registro():
    """
    Rota para registro de um novo usuário, recebe nome, email e senha.

    Tanto login como registro utilizam a página login.html.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if current_user.is_authenticated:
        return redirect('/inicio')

    nomeFormulario = request.args.get('nome')
    emailFormulario = request.args.get('email')
    senhaFormulario = request.args.get('senha')

    # TODO: usuário vai receber um erro assim que entrar no site, pois o valor, quando entrar, vai ser None.
    if None or '' in (nomeFormulario, emailFormulario, senhaFormulario):
        erro = 'Valores não podem estar vazios.'
    else:
        if Usuario.query.filter_by(email=emailFormulario).first() is not None:
            erro = 'Este usuário já existe.'
        else:
            senhaHash = bcrypt.generate_password_hash(senhaFormulario).decode('utf-8')

            novo_usuario = Usuario(nome=nomeFormulario, 
                                   email=emailFormulario, 
                                   pwhash=senhaHash)
            db.session.add(novo_usuario)
            db.session.commit()

            login_user(novo_usuario)

            resposta = make_response(redirect('/inicio'))
            return resposta
    return render_template('login.html', erro=erro, titulo='Cadastro')


def logout():
    resposta = make_response(redirect('/inicio'))
    logout_user()
    return resposta