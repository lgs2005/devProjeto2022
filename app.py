from flask import render_template
from flask_login import login_required

from rotas import ROTAS
from init import app, db

db.create_all()

def adicionar_rotas(rotas):
    '''
    Adiciona/Cadastra as rotas ao objeto app.
    Quando a rota possui mais de uma opção de cadastramento,
    por exemplo 'view_func' e 'method', esta função adiciona-a 
    mesmo assim.
    '''
    for rota, options in rotas.items():
        if type(options) == dict:
            app.add_url_rule(rota, **options)
        else:
            app.add_url_rule(rota, view_func=options)

adicionar_rotas(ROTAS)

if __name__ == '__main__':
    app.run(debug=True)
