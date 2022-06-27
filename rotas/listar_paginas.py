from flask import jsonify, render_template
from flask_login import current_user

from modelos import Pagina
from rotas.utils import requer_login


@requer_login
def rota_listar_paginas():
    """Lista as páginas do usuário da 
    sessão atual.

    Returns:
        Response: objeto json com as páginas.
    """
    paginas: 'list[Pagina]' = Pagina.query.filter_by(usuario=current_user).all()
    resposta = jsonify([p.json() for p in paginas])

    return resposta


def rota_teste_barra_lateral():
    return render_template('barra_lateral.html')


def adicionar_rotas():
    return {
        '/listar_paginas': rota_listar_paginas,
        '/teste_barra_lateral': rota_teste_barra_lateral,
    }
