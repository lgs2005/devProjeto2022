from http.client import OK, UNAUTHORIZED, INTERNAL_SERVER_ERROR, NOT_FOUND

from flask import make_response, request, abort
from flask_login import current_user

from init import caminho_base
from modelos import Usuario, Pagina, Compartilhamento


PASTA_DE_PAGINAS = f'{caminho_base}/paginas'


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

def requerir_acesso(usuario: Usuario, pagina: Pagina):
    '''
    Requerir acesso à uma página.

    Recebe Usuario e Página.
    Retorna "Acesso não autorizado", caso não existe um 
    compartilhamento de páginas.
    '''
    if pagina.id_usuario != usuario.id:
        compartilhamento = Compartilhamento.query \
            .filter_by(usuario=usuario, pagina=pagina).first()
        if compartilhamento == None:
            abort(UNAUTHORIZED, 'Você não tem acesso a esta página.')
    return True


def abrir_pagina(pagina: Pagina, modo: str):
    '''
    Abrir página.
    
    Recebe Página e modo (write ou read).
    '''
    try:
        return open(f'{PASTA_DE_PAGINAS}/{pagina.caminho}.json', mode=modo)
    except FileNotFoundError:
        if modo == 'w':
            return abrir_pagina(pagina, 'x')
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)