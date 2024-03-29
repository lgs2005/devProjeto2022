from datetime import datetime, timedelta
import os

from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK, UNAUTHORIZED

from flask import abort, jsonify, request
from flask_login import current_user
from sqlalchemy import null
from init import app, db, catimg
from modelos import Pagina, Usuario
from paginas import caminho_para_pagina, criar_arquivo_pagina

from rotas.utils import api_requer_login, validar_objeto


@app.route('/api/criar-pagina', methods=["POST"])
@api_requer_login
def rota_api_criar_pagina():
    """Rota de criação de página.
    Recebe dados em json do front end: nome da página

    Returns:
        Response (jsonify): resposta em json contendo sucesso e erro.
        INTERNAL SERVER ERROR (cod. 500): erro do servidor. inválido

    """

    dados = validar_objeto(request.get_json(), {
        'nome': str
    })

    nome: str = dados['nome']
    arquivo = criar_arquivo_pagina(nome)
    sucesso = False

    print(arquivo)

    if arquivo == None:
        abort(INTERNAL_SERVER_ERROR)

    nova_pagina = Pagina(
        nome=nome, id_usuario=current_user.id, caminho_id=arquivo)

    db.session.add(nova_pagina)
    db.session.commit()

    sucesso = True

    return jsonify({
        'sucesso': sucesso,
    })


@app.route("/api/conteudo/<int:id>", methods=["GET", "PUT"])
@api_requer_login
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

    if not pagina.existe_compartilhamento(current_user):
        abort(UNAUTHORIZED)

    try:
        arquivo_pagina = open(
            caminho_para_pagina(pagina.caminho_id),
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
def deletar_pagina(id:int):
    pagina: Pagina = Pagina.query.get_or_404(id)

    if not pagina.existe_compartilhamento(current_user):
        abort(UNAUTHORIZED)

    pagina.excluir_em = datetime.utcnow() + timedelta(seconds=10)
    db.session.commit()
    
    return catimg(OK), OK

# ok eu não tenho certeza quando isso deveria acontecer
# então porenquanto essa função fica aqui mesmo
def limpar_paginas_excluidas():
    paginas_para_excluir = Pagina.query\
        .filter(Pagina.excluir_em != None)\
        .filter(Pagina.excluir_em <= datetime.utcnow())\
        .all()

    print(paginas_para_excluir)

    for pagina in paginas_para_excluir:
        deletar_pagina_definitivamente(pagina)

def deletar_pagina_definitivamente(pagina: Pagina):
    try:
        os.remove(caminho_para_pagina(pagina.caminho_id))
        Pagina.query.filter_by(id=pagina.id).delete()
        db.session.commit()
    except FileNotFoundError:
        pass
    except OSError:
        pass

@app.route("/api/deletar/pagina/<int:id>", methods=['DELETE'])
def rota_deletar_pagina_definitivamente(id:int):
    pagina: Pagina = Pagina.query.get_or_404(id)

    if not pagina.existe_compartilhamento(current_user):
        abort(UNAUTHORIZED)

    deletar_pagina_definitivamente(pagina)
    
    return catimg(OK), OK

@app.route("/api/recuperar/pagina/<int:id>", methods=['POST'])
def recuperar_pagina(id:int):
    pagina: Pagina = Pagina.query.get_or_404(id)

    if not pagina.existe_compartilhamento(current_user):
        abort(UNAUTHORIZED)

    pagina.excluir_em = None
    db.session.commit()
    
    return catimg(OK), OK
