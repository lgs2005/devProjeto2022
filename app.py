from flask import render_template
from flask_login import login_required

from rotas import ROTAS
from init import app, db

@app.route('/hello')
def hello_world():
    # https://www.youtube.com/watch?v=dwDns8x3Jb4
    return '<img src=\'https://media1.giphy.com/media/mf8UbIDew7e8g/200.gif\'/>' + \
        ' '.join(['<p>around the world</p>'] * 144)


@login_required
def rota_inicio():

    return render_template('inicio.html')


db.create_all()


def adicionar_rotas(rotas):
    '''
    Adiciona/Cadastra as rotas ao objeto app.
    Quando a rota possui mais de uma opção de cadastramento,
    por exemplo 'view_func' e 'method', esta função adiciona-a 
    mesmo assim.

    Se as 'options' forem um dicionário, ou seja, mais de uma opção.
    iiiiiii nao terminou a documentação.....
    '''
    for rota, options in rotas.items():
        if type(options) == dict:
            app.add_url_rule(rota, **options)
        else:
            app.add_url_rule(rota, view_func=options)


outras_rotas = {
    '/': rota_inicio,
    '/inicio': rota_inicio,
}

adicionar_rotas(outras_rotas)
adicionar_rotas(ROTAS)

if __name__ == '__main__':
    app.run(debug=True)
