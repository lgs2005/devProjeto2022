import os
from datetime import datetime, timedelta, timezone
from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED

from flask import abort, jsonify, request
from flask_jwt_extended import get_current_user, jwt_required
from init import app, catimg, db
from modelos import Pagina, Usuario
from paginas import caminho_para_pagina, criar_arquivo_pagina

from rotas.utils import get_campos


@app.post('/api/pagina/criar')
@jwt_required()
def rota_api_criar_pagina():
    """
        Rota de criação de página.
    Recebe dados em json do front end: nome da página

    Returns:
        Response (jsonify): resposta em json contendo sucesso e erro.
        INTERNAL SERVER ERROR (cod. 500): erro do servidor. inválido
    """
    nome = get_campos(str, 'name')
    pasta_id = get_campos(int, 'folder')

    arquivo = criar_arquivo_pagina()

    if arquivo == None:
        abort(INTERNAL_SERVER_ERROR)

    print('Arquivo criado: ' + arquivo)

    pagina = Pagina(
        nome=nome,
        arquivo=arquivo,
        autor=Usuario.atual(),
        pasta_id=pasta_id,
        data_criacao=datetime.now(timezone.utc)
    )

    db.session.add(pagina)
    db.session.commit()

    return jsonify(pagina.dados())


@app.get('/api/pagina/listar')
@jwt_required()
def rota_listar_paginas():
    """
        Rota listagem de páginas do usuário da 
    sessão atual.

        Returns:
                GET:
                        OK (cod. 200): páginas em JSON.
    """
    paginas = Pagina.query.filter_by(autor=Usuario.atual()).all()
    dados = [ p.dados() for p in paginas ]
    return jsonify(dados)


@app.route("/api/conteudo/<int:id>", methods=["GET", "PUT"])
@jwt_required()
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

    if not pagina.tem_acesso(Usuario.atual()):
        abort(UNAUTHORIZED)

    try:
        arquivo_pagina = open(
            caminho_para_pagina(pagina.arquivo),
            'r' if request.method == "GET" else 'w'
        )

        if request.method == "GET":
            return arquivo_pagina.read()
        else:
            novo_conteudo = get_campos(str, 'content')

            arquivo_pagina.truncate()
            arquivo_pagina.write(novo_conteudo)
            return catimg(OK), OK

    except FileNotFoundError:
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)
    finally:
        arquivo_pagina.close()


@app.route("/api/excluir/pagina/<int:id>", methods=['DELETE'])
def deletar_pagina(id: int):
    pagina = Pagina.query.get_or_404(id)

    if not pagina.tem_acesso(Usuario.atual()):
        abort(UNAUTHORIZED)

    pagina.data_excluir = datetime.now(timezone.utc) + timedelta(days=30)
    db.session.commit()

    return catimg(OK), OK


def limpar_paginas_excluidas():
    paginas_para_excluir = Pagina.query\
        .filter(Pagina.data_excluir != None)\
        .filter(Pagina.data_excluir > datetime.now(timezone.utc))\
        .all()

    for pagina in paginas_para_excluir:
        try:
            os.remove(caminho_para_pagina(pagina.arquivo))
            db.session.delete(pagina)
        except FileNotFoundError:
            pass
        except OSError:
            pass
