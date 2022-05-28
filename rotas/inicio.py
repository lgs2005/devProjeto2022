from flask import render_template, redirect
from flask_login import login_required, current_user


@login_required
def rota_inicio():
    """
    Rota início/home.

    Template utilizado: 'inicio.html'.
    Por enquanto só serve como um "ponto de partida".
    """
    return render_template('inicio.html')


def rota_default():
    """
    Rota default.
    Esta rota só existe para o usuário poder acessar o site normalmente 
    sem ter "POR FAVOR ENTRE EM SUA CONTA PARA VISUALIZAR ESTA PÁGINA" 
    na sua primeira vez.
    """
    return redirect('/inicio' if current_user.is_authenticated else '/login')


def adicionar_rotas():
    return {
        '/': rota_default,
        '/inicio': rota_inicio,
    }
