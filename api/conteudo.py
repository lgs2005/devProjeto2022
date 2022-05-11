from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED

from flask import abort, make_response, request
from modelos import Compartilhamento, Pagina, Usuario

from api.util import requerir_usuario

PASTA_DE_PAGINAS = "./paginas"


def requerir_acesso(usuario: Usuario, pagina: Pagina):
    if pagina.id_usuario != usuario.id:
        compartilhamento = Compartilhamento.query.filter_by(
            id_usuario=usuario.id, id_pagina=pagina.id).first()
        if compartilhamento == None:
            abort(UNAUTHORIZED, "Você não tem acesso a esta página.")

    return True


def rota_retornar_conteudo(id: int = None):
    usuario = requerir_usuario()
    pagina: Pagina = Pagina.query.filter_by(id=id).first_or_404()
    requerir_acesso(pagina, usuario)

    try:
        arquivo_pagina = open(
            f"{PASTA_DE_PAGINAS}/{pagina.conteudo}.json", mode='r')
    except FileNotFoundError:
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)

    conteudo = arquivo_pagina.read()

    return conteudo


# atualiza o conteúdo da página
def rota_publicar_conteudo(id: int = None):
    usuario = requerir_usuario()
    pagina: Pagina = Pagina.query.filter_by(id=id).first_or_404()
    requerir_acesso(pagina, usuario)

    try:
        arquivo_pagina = open(
            f"{PASTA_DE_PAGINAS}/{pagina.conteudo}.json", mode='w')
    except FileNotFoundError:
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)

    dados = request.data
    arquivo_pagina = arquivo_pagina.write(dados)

    return make_response(OK)


def adicionar_rotas():
    return {
        '/retornar_conteudo/<int:id>': rota_retornar_conteudo,

        '/publicar_conteudo/<int:id>': {
            'view_func': rota_publicar_conteudo,
            'methods': ['POST']
        }
    }
