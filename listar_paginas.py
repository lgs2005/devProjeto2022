from flask import jsonify
from init import *
from modelos import Pagina

@app.route("/")
def inicio():
    return 'Sistema de cadastro de paginas.'+\
        '<a href="/listar_paginas">Operação listar</a>'

@app.route("/listar_paginas")
def listar_paginas():
    # obter as paginas do cadastro
    paginas = db.session.query(Pagina).all()
    # aplicar o método json que a classe pagina possui a cada elemento da lista
    paginas_em_json = [ x.json() for x in paginas ]
    # converter a lista do python para json
    resposta = jsonify(paginas_em_json)
    # permitir resposta para pedidos oriundos de outras tecnologias
    resposta.headers.add("Access-Control-Allow-Origin", "*")
    return resposta 

# iniciar o servidor web
if __name__ == "__main__":
    app.run(debug=True)    