from os import abort
from flask import jsonify, render_template

from login import usuario_logado
from modelos import Pagina

def rota_listar_paginas():
    usuario = usuario_logado()

    if usuario == None:
        abort(403)

    paginas: 'list[Pagina]' = Pagina.query.filter_by(id_usuario=usuario.id).all()
    resposta = jsonify([p.json() for p in paginas])

    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta

def rota_teste_barra_lateral():
    return render_template('listar_paginas.html')

def adicionar_rotas():
    return {
        '/listar_paginas': rota_listar_paginas,
        '/teste_barra_lateral': rota_teste_barra_lateral,
    }