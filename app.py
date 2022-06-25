from rotas import ROTAS
from init import app, db

@app.route('/hello')
def hello_world():
    # https://www.youtube.com/watch?v=dwDns8x3Jb4
    return '<img src=\'https://media1.giphy.com/media/mf8UbIDew7e8g/200.gif\'/>' + \
        ' '.join(['<p>around the world</p>'] * 144)


def adicionar_rotas(rotas):
    '''
    Adiciona as rotas ao objeto app.
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
    db.create_all()
    app.run(debug=True)
