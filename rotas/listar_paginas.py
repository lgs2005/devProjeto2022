from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from init import app
from modelos import Pagina

@app.route("/api/listar-paginas", methods=["GET"])
@jwt_required()
def rota_listar_paginas():
    """Lista as páginas do usuário da 
    sessão atual.

    Returns:
        Response: objeto json com as páginas.
    """
    paginas: 'list[Pagina]' = Pagina.query \
        .filter_by(usuario=current_user).all()

    resposta = jsonify([p.json() for p in paginas])

    return resposta
