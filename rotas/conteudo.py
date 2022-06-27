from http.client import OK, UNAUTHORIZED, INTERNAL_SERVER_ERROR, NOT_FOUND

from flask import request, abort, jsonify
from flask_login import current_user

from modelos import Pagina, Compartilhamento
from paginas import criar_arquivo_pagina
from rotas.utils import requer_login, validar_objeto
from init import db


@requer_login
def rota_api_criar_pagina():
    """Rota de criação de página.
    Recebe dados em json do front end: nome da página

    Returns:
        Response (jsonify): resposta em json contendo ´sucesso´ e ´erro´.
        INTERNAL SERVER ERROR (cod. 500): erro do servidor. inválido

    """

    dados = validar_objeto(request.get_json(), {
        'nome': str
    })

    nome: str = dados['nome']
    arquivo = criar_arquivo_pagina()
    sucesso = False

    if arquivo == None:
        abort(INTERNAL_SERVER_ERROR)

    nova_pagina = Pagina(nome=nome, id_usuario=current_user.id, caminho=arquivo)

    db.session.add(nova_pagina)
    db.session.commit()

    sucesso = True

    return jsonify({
        'sucesso': sucesso,
    })


@requer_login
def rota_api_conteudo(id: int = None):
    """Gerencia determinada página do usuário, passando o
    id da mesma.
    Realiza as operações GET (método read file) e POST (método
    write file).

    Args:
        id (int, opcional): id da página. Padrão None.

    Returns:
        GET:
            str: leitura da página. válido
        
        POST:
            OK (cod. 200): sucesso. válido

        UNAUTHORIZED (cod. 401): compartilhamento de página não
        autorizado. inválido.
        NOT_FOUND (cod. 404): página não encontrada. inválido
        INTERNAL_SERVER_ERROR (cod. 500): erro do servidor. inválido
    """

    pagina: Pagina = Pagina.query.get_or_404(id)
    
    if pagina.id_usuario != current_user.id:
        compartilhamento = Compartilhamento.query \
            .filter_by(usuario=current_user, pagina=pagina).first()

        if compartilhamento == None:
            abort(UNAUTHORIZED)

    if request.method == "GET":
        try:
            arquivo_pagina = open(pagina.caminho, 'r')
            return arquivo_pagina.read()
        except FileNotFoundError:
            abort(NOT_FOUND)
        except OSError:
            abort(INTERNAL_SERVER_ERROR)

    elif request.method == "POST":
        try:
            arquivo_pagina = open(pagina.caminho, 'w')
            arquivo_pagina.truncate()
            arquivo_pagina.write(request.get_data().decode('utf-8', 'ignore'))
            return OK
        except FileNotFoundError:
            abort(NOT_FOUND)
        except OSError:
            abort(INTERNAL_SERVER_ERROR)


def adicionar_rotas():
    return {
        '/api/criar_pagina': {
            'methods': ["POST"],
            'view_func': rota_api_criar_pagina,
        },

        '/api/conteudo/<int:id>': {
            'methods': ["GET", "POST"],
            'view_func': rota_api_conteudo,
        }
    }