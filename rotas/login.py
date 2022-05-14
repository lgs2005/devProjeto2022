from flask import request, redirect, render_template
from flask_login import current_user, login_user, logout_user

from modelos import Usuario
from init import bcrypt, db


def rota_login():
    """
    Rota para login do usuário, recebe nome, email e senha.

    Tanto login como registro utilizam a página login.html.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if current_user.is_authenticated:
        return redirect('/')

    email = request.args.get('email')
    senha = request.args.get('senha')

    erro = None

    if '' not in (email, senha) and None not in (email, senha):
        usuario: Usuario = Usuario.query.filter_by(email=email).first()

        if usuario == None:
            erro = 'Este usuário não existe.'
        elif not bcrypt.check_password_hash(usuario.pwhash, senha):
            erro = 'Senha incorreta.'
        else:
            login_user(usuario)
            return redirect('/')

    return render_template('login.html', titulo='Login', erro=erro)


def rota_registro():
    """
    Rota para registro de um novo usuário, recebe nome, email e senha.

    Tanto login como registro utilizam a página login.html.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if current_user.is_authenticated:
        return redirect('/')

    nome = request.args.get('nome')
    email = request.args.get('email')
    senha = request.args.get('senha')

    erro = None

    if '' not in (nome, email, senha) and None not in (nome, email, senha):
        if Usuario.query.filter_by(email=email).first() != None:
            erro = 'Este usuário já existe'
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

            return redirect('/')

    return render_template('login.html', titulo='Cadastro', erro=erro)


def rota_logout():
    logout_user()
    return redirect('/')


def adicionar_rotas():
    return {
        '/registrar': rota_registro,
        '/login': rota_login,
        '/logout': rota_logout,
    }
