from init import app, db
from flask import send_from_directory

# para registrar na base de dados
import modelos

# imports para registrar as rotas
import rotas.conteudo
import rotas.listar_paginas
import rotas.usuario

@app.route('/', methods=['GET'])
def rota_react():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    db.create_all()
