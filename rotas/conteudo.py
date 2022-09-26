from datetime import datetime, timedelta, timezone
import os

from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED

from flask import abort, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user

from init import app, db, catimg
from modelos import Pagina, Usuario
from paginas import caminho_para_pagina, criar_arquivo_pagina

from rotas.utils import validar_dados


@app.route('/api/pagina/criar', methods=["POST"])
@jwt_required()
def rota_api_criar_pagina():
    """
	Rota de criação de página.
    Recebe dados em json do front end: nome da página

    Returns:
        Response (jsonify): resposta em json contendo sucesso e erro.
        INTERNAL SERVER ERROR (cod. 500): erro do servidor. inválido
    """
    usuario: Usuario = get_current_user()
    dados = validar_dados(request.get_json(), {
        'nome': str
    })

    arquivo = criar_arquivo_pagina()

    if arquivo == None:
        abort(INTERNAL_SERVER_ERROR)

    print('Arquivo criado: ' + arquivo)

    pagina = Pagina(
        nome=dados['nome'],
        arquivo=arquivo,
        autor=usuario,

        favorito=False,
        data_criacao=datetime.now(timezone.utc)
    )

    db.session.add(pagina)
    db.session.commit()

    return jsonify(pagina.dados())

@app.route('/api/pagina/listar', methods=['GET'])
@jwt_required()
def rota_listar_paginas():
    """
	Rota listagem de páginas do usuário da 
    sessão atual.

	Returns:
		GET:
			OK (cod. 200): páginas em JSON.
    """
    usuario: Usuario = get_current_user()
    paginas: 'list[Pagina]' = Pagina.query \
        .filter_by(usuario=usuario).all()

    resposta = jsonify([p.dados() for p in paginas])

    return resposta


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

    usuario: Usuario = get_current_user()
    pagina: Pagina = Pagina.query.get_or_404(id)

    if not pagina.tem_acesso(usuario):
        abort(UNAUTHORIZED)

    try:
        arquivo_pagina = open(
            caminho_para_pagina(pagina.arquivo),
            'r' if request.method == "GET" else 'w'
        )

        if request.method == "GET":
            return arquivo_pagina.read()
        else:
            arquivo_pagina.truncate()
            arquivo_pagina.write(request.get_data().decode('utf-8', 'ignore'))
            return catimg(OK), OK

    except FileNotFoundError:
        abort(NOT_FOUND)
    except OSError:
        abort(INTERNAL_SERVER_ERROR)


@app.route("/api/excluir/pagina/<int:id>", methods=['DELETE'])
def deletar_pagina(id: int):
    usuario: Usuario = get_current_user()
    pagina: Pagina = Pagina.query.get_or_404(id)

    if not pagina.tem_acesso(usuario):
        abort(UNAUTHORIZED)
    
    pagina.data_excluir = datetime.now(timezone.utc) + timedelta(days=30)
    db.session.commit()
    
    return catimg(OK), OK

def limpar_paginas_excluidas():
    paginas_para_excluir: list[Pagina] = Pagina.query\
        .filter(Pagina.data_excluir  != None)\
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
