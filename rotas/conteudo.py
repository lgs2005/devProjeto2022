from http.client import OK, UNAUTHORIZED, INTERNAL_SERVER_ERROR, NOT_FOUND

from flask import request, abort
from flask_login import current_user

from modelos import Pagina, Compartilhamento
from paginas import caminho_para_pagina, reservar_arquivo
from rotas.utils import requer_login, validar_objeto
from init import db


@requer_login
def rota_api_criar_pagina():
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
def rota_api_conteudo(id: int = None):
    pagina: Pagina = Pagina.query.get_or_404(id)
    
    # conferir se o usuário tem acesso
    if pagina.id_usuario != current_user.id:
        compartilhamento = Compartilhamento.query \
            .filter_by(usuario=current_user, pagina=pagina).first()

        if compartilhamento == None:
            abort(UNAUTHORIZED)

    caminho = caminho_para_pagina(pagina.caminho)

    if request.method == "GET":
        try:
            arquivo_pagina = open(caminho, 'r')
            return arquivo_pagina.read()
        except FileNotFoundError:
            abort(NOT_FOUND)
        except OSError:
            abort(INTERNAL_SERVER_ERROR)

    elif request.method == "POST":
        try:
            arquivo_pagina = open(caminho, 'w')
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