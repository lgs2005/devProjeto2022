from http.client import (BAD_REQUEST, 
                         GONE, 
                         UNAUTHORIZED, 
                         NOT_FOUND, 
                         INTERNAL_SERVER_ERROR, 
                         OK)
from flask import abort, request, make_response
from flask_login import current_user

from modelos import Usuario, Compartilhamento, Pagina

import os

from paginas_usuario import path

thisFolderPath = os.getcwd

def solicitar_acesso(usuario: Usuario, pagina: Pagina):
    if pagina.id_usuario != usuario.id:
        compartilhamento = Compartilhamento.quary.filter_by(
            id_usuario=usuario.id, id_pagina=pagina.id).first()
        if compartilhamento == None:
            abort(UNAUTHORIZED, "Você não possui acesso a essa página.")
    return True


def rota_retornar_conteudo(id: int = None):
    usuario = current_user
    pagina: Pagina = Pagina.query.filter_by(id=id).first_or_404()
    solicitar_acesso(pagina=pagina, usuario=usuario)

    try:
        arquivo_pagina = open(f"{path}\\{pagina.conteudo}.json", mode='r')
    except FileNotFoundError:
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)

    conteudo = arquivo_pagina.read()
    return conteudo


def rota_publicar_conteudo(id: int = None):
    usuario = current_user
    pagina: Pagina = Pagina.query.filter_by(id=id).first_or_404()
    solicitar_acesso(pagina=pagina, usuario=usuario)

    try:
        arquivo_pagina = open(f"{path}\\{pagina.conteudo}.json", mode='w')
    except FileNotFoundError:
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)

    dados = request.data
    arquivo_pagina = arquivo_pagina.write(dados)
    return make_response(OK)


