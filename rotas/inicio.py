from flask import render_template, redirect
from flask_login import current_user


def rota_default():
    """
    Rota default, usuário deve estar autenticado, senão
    é redirecionado para `/login`
    """
    return render_template('barra_lateral.html') if current_user.is_authenticated else redirect('/login')


def adicionar_rotas():
    return {
        '/': rota_default,
    }
