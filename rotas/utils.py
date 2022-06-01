from http.client import UNAUTHORIZED, NOT_FOUND, INTERNAL_SERVER_ERROR

from flask import abort

from init import caminho_base
from modelos import Compartilhamento, Pagina, Usuario


PASTA_DE_PAGINAS = f'{caminho_base}/paginas'


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
