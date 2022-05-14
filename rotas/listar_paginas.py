from flask import jsonify, render_template
from modelos import Pagina

from rotas.util import requerir_usuario


def rota_listar_paginas():
    usuario = requerir_usuario()

    paginas: 'list[Pagina]' = Pagina.query.filter_by(usuario=usuario).all()
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
