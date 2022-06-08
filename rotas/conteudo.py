from http.client import OK, UNAUTHORIZED, INTERNAL_SERVER_ERROR, NOT_FOUND

from flask import make_response, request, abort
from flask_login import current_user

from modelos import Usuario, Pagina, Compartilhamento
from paginas import reservar_arquivo
from rotas.utils import requer_login, validar_objeto
from init import db

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

#       #
# ROTAS #
#       #

@requer_login
def rota_criar_pagina():
    dados = validar_objeto(request.get_json(), {
        'nome': str
    })

    nome: str = dados['nome']
    arquivo = reservar_arquivo()

    if arquivo == None:
        abort(INTERNAL_SERVER_ERROR)

    nova_pagina = Pagina(nome=nome, usuario_id=current_user.id, caminho=arquivo)

    db.session.add(nova_pagina)
    db.session.commit()

    return OK

@requer_login
def rota_conteudo(id: int = None):
    '''
    documentação FODA
    '''
    pagina: Pagina = Pagina.query.get_or_404(id)
    requerir_acesso(current_user, pagina)

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