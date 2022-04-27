from http.client import BAD_REQUEST, GONE, UNAUTHORIZED
from flask import abort, make_response, redirect, request
from init import app
from login import usuario_logado
from modelos import Compartilhamento, Pagina


PASTA_DE_PAGINAS = "./paginas"


def rota_retornar_conteudo(id=None):
    if id == None:
        abort(BAD_REQUEST)
    
    usuario = usuario_logado()
    if usuario == None:
        abort(UNAUTHORIZED)

    try:
        id = int(id)
    except ValueError:
        abort(BAD_REQUEST)

    pagina: Pagina = Pagina.query.filter_by(id=id).first_or_404()

    if pagina.id_usuario != usuario.id:
        # procurar por um compartilhamento

        compartilhamento = Compartilhamento.query.filter_by(id_usuario=usuario.id, id_pagina=pagina.id).first()

        if compartilhamento == None:
            abort(UNAUTHORIZED)


    # a este ponto o usuário deve ter acesso
    
    try:
        arquivo_pagina = open(f"{PASTA_DE_PAGINAS}/{pagina.conteudo}.json")
    except FileNotFoundError:
        return abort(GONE)

    conteudo = arquivo_pagina.read()

    return conteudo