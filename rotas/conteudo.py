from http.client import OK

from flask import make_response, request
from flask_login import current_user

from .utils import requerir_acesso, abrir_pagina
from modelos import Pagina


def rota_retornar_conteudo(id: int = None):
    '''
    Rota retornar conteúdo.

    Recebe id: inteiro.
    Modo de leitura -> Read.
    Se o usuário não tiver acesso a esta página,
    é retornado um erro 404.
    '''
    usuario = current_user
    pagina: Pagina = Pagina.query.get_or_404(id)

    requerir_acesso(usuario, pagina)

    arquivo_pagina = abrir_pagina(pagina, 'r')
    conteudo = arquivo_pagina.read()

    return conteudo


def rota_publicar_conteudo(id: int = None):
    '''
    Rota publicar conteúdo (salvar conteúdo).

    Recebe id: inteiro.
    Modo leitura -> Write.
    Se o usuário não tiver acesso a esta página,
    é retornado um erro 404.
    '''
    usuario = current_user
    pagina: Pagina = Pagina.query.get_or_404(id)

    requerir_acesso(usuario, pagina)

    arquivo_pagina = abrir_pagina(pagina, 'w')
    dados = request.get_data().decode()

    arquivo_pagina.write(dados)
    return make_response('Sucesso', OK)


def adicionar_rotas():
    return {
        '/retornar_conteudo/<int:id>': rota_retornar_conteudo,
        '/publicar_conteudo/<int:id>': {
            'view_func': rota_publicar_conteudo,
            'methods': ['POST']
        }
    }
