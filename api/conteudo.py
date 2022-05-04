from http.client import BAD_REQUEST, NOT_FOUND, UNAUTHORIZED
from flask import abort
from api.util import int_or_badrequest
from login import usuario_logado
from modelos import Compartilhamento, Pagina


PASTA_DE_PAGINAS = "./paginas"


def rota_retornar_conteudo(id=None):
    if id == None:
        abort(BAD_REQUEST)
    
    usuario = usuario_logado()
    if usuario == None:
        abort(UNAUTHORIZED)

    id = int_or_badrequest()
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
        return abort(NOT_FOUND)

    conteudo = arquivo_pagina.read()

    return conteudo


# atualiza o conteúdo da página
def rota_publicar_conteudo(id=None):
    pass


def adicionar_rotas():
    return {
        '/retornar_conteudo/<id>': rota_retornar_conteudo,

        '/publicar_conteudo/<id>': {
            'view_func': rota_publicar_conteudo,
            'methods': ['POST']
        }
    }