from flask import jsonify, render_template
from flask_login import current_user, login_required

from modelos import Pagina


@login_required
def rota_listar_paginas():
    """Lista as páginas do usuário
    da seção atual.

    Returns:
        Response: objeto json.
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
