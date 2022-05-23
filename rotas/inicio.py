from flask import render_template
from flask_login import login_required


@login_required
def rota_inicio():
    """
    Rota início/home.

    Template utilizado: 'inicio.html'.
    Por enquanto só serve como um "ponto de partida".
    """
    return render_template('inicio.html')


def adicionar_rotas():
    return {
        '/': rota_inicio,
        '/inicio': rota_inicio,
    }