from flask import jsonify
from flask_login import current_user
from init import app
from modelos import Pagina
from rotas.conteudo import limpar_paginas_excluidas

from rotas.utils import api_requer_login

@app.route("/api/listar-paginas", methods=["GET"])
@api_requer_login
def rota_listar_paginas():
    """Lista as páginas do usuário da 
    sessão atual.

    Returns:
        Response: objeto json com as páginas.
    """
    paginas: 'list[Pagina]' = Pagina.query \
        .filter_by(usuario=current_user).all()

    limpar_paginas_excluidas()
    resposta = jsonify([p.json() for p in paginas])

    return resposta
