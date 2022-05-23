from flask import request, redirect, render_template, url_for, flash
from flask_login import current_user, login_user, logout_user

from modelos import Usuario
from init import bcrypt, db


def rota_login():
    """
    Rota para login do usuário, recebe nome, email e senha.

    Template utilizado: 'login.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if current_user.is_authenticated:
        # Se assume que o usuário já está logado. 
        return redirect(url_for('rota_inicio'))

    email = request.args.get('email')
    senha = request.args.get('senha')

    if '' not in (email, senha) and None not in (email, senha):
        usuario: Usuario = Usuario.query.filter_by(email=email).first()

        if usuario == None:
            flash('Este usuário não existe.', 'danger')
        elif not bcrypt.check_password_hash(usuario.pwhash, senha):
            flash('Senha incorreta.', 'danger')
        else:
            login_user(usuario)
            return redirect(url_for('rota_inicio'))

    return render_template('login.html', tituloPagina='Login')


def rota_registro():
    """
    Rota para registro de um novo usuário, recebe nome, email e senha.

    Template utilizado: 'registro.html'.
    Caso o usuário já estiver logado, será redirecionado para '/inicio'.
    """
    if current_user.is_authenticated:
        # Se assume que o usuário já está logado. 
        return redirect(url_for('rota_inicio'))

    nome = request.args.get('nome')
    email = request.args.get('email')
    senha = request.args.get('senha')

    erro = None

    if '' not in (nome, email, senha) and None not in (nome, email, senha):
        if Usuario.query.filter_by(email=email).first() != None:
            flash('Este usuário já existe.', 'info')
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

            return redirect(url_for('rota_inicio'))

    return render_template('registro.html', tituloPagina='Cadastro', erro=erro)


def rota_logout():
    """
    Rota para logout do usuário.
    """
    logout_user()
    return redirect(url_for('rota_inicio'))


def adicionar_rotas():
    return {
        '/registrar': rota_registro,
        '/login': rota_login,
        '/logout': rota_logout,
    }