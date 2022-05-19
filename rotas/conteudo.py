from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED

from flask import abort, make_response, request
from init import caminho_base
from modelos import Compartilhamento, Pagina, Usuario

from rotas.util import requerir_usuario


PASTA_DE_PAGINAS = f'{caminho_base}/paginas'


def abrir_pagina(pagina: Pagina, modo: str):
    try:
        return open(f'{PASTA_DE_PAGINAS}/{pagina.caminho}.json', mode=modo)
    except FileNotFoundError:
        if modo == 'w':
            return abrir_pagina(pagina, 'x')
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)


def requerir_acesso(usuario: Usuario, pagina: Pagina):
    if pagina.id_usuario != usuario.id:
        compartilhamento = Compartilhamento.query \
            .filter_by(usuario=usuario, pagina=pagina).first()

        if compartilhamento == None:
            abort(UNAUTHORIZED, "Você não tem acesso a esta página.")

    return True


def rota_retornar_conteudo(id: int = None):
    usuario = requerir_usuario()
    pagina: Pagina = Pagina.query.get_or_404(id)

    requerir_acesso(usuario, pagina)

    arquivo_pagina = abrir_pagina(pagina, 'r')
    conteudo = arquivo_pagina.read()

    return conteudo


# atualiza o conteúdo da página
def rota_publicar_conteudo(id: int = None):
    usuario = requerir_usuario()
    pagina: Pagina = Pagina.query.get_or_404(id)

    requerir_acesso(usuario, pagina)

    arquivo_pagina = abrir_pagina(pagina, 'w')
    dados = request.get_data().decode()

    arquivo_pagina.write(dados)
    return make_response('sucesso!', OK)


# caralho esse codigo ta muito feio
# nem sei o que fazer sobre isso entao vai assim mesmo

def adicionar_rotas():
    return {
        '/retornar_conteudo/<int:id>': rota_retornar_conteudo,
        '/publicar_conteudo/<int:id>': {
            'view_func': rota_publicar_conteudo,
            'methods': ['POST']
        }
    }