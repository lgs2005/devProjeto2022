from werkzeug.exceptions import HTTPException as WerkzeugHTTPException
from init import app, catimg, db

# para registrar na base de dados
import modelos

# imports para registrar as rotas
import rotas.conteudo
import rotas.inicio
import rotas.listar_paginas
import rotas.perfil
import rotas.usuario

@app.route('/hello')
def hello_world():
    """Super Mario Rapper"""
    return '<img src=\'https://c.tenor.com/3fnHh1WgOIwAAAAC/rapping-mario-mario.gif\'/>'


@app.errorhandler(WerkzeugHTTPException)
def error_cat(e: WerkzeugHTTPException):
    return catimg(e.code), e.code


@app.errorhandler(Exception)
def internal_error_cat(e: Exception):
    print(f'\n\n{e}\n\n')
    return catimg(500), 500


if __name__ == '__main__':
    db.create_all()
