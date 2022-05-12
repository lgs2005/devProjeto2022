from flask import render_template

from config import app, db, databasePath
from usuario.rotas_usuario import rota_login, rota_registro, logout
from paginas.pagina import rota_retornar_conteudo, rota_publicar_conteudo

# import os


# if os.path.exists(databasePath):
#     os.remove(databasePath)
# db.create_all()

# TODO: Validar formulários ao submeter

def rota_inicio(): 
    return render_template('inicio.html')

todas_as_rotas = {
    '/': rota_inicio,
    '/inicio': rota_inicio,

    '/registrar': rota_registro,
    '/login': rota_login,
    '/logout': logout,
    
    '/retornar_conteudo/<int:id>': rota_retornar_conteudo,
    '/publicar/<int:id>': {
        'view_func': rota_publicar_conteudo,
        'methods': ['POST']
    }
}

def adicionar_rotas(rotas):
    '''
    Adiciona/Cadastra as rotas ao objeto app.
    Quando a rota possui mais de uma opção de cadastramento,
    por exemplo 'view_func' e 'method', esta função adiciona-a 
    mesmo assim.

    Se as 'options' forem um dicionário, ou seja, mais de uma opção.
    '''
    for rota, options in rota.items():
        if type(options) == dict:
            app.add_url_rule(rota, **options)
        else:
            app.add_url_rule(rota, view_func=options)
        # TODO: não vai funcionar se só tiver isso:
        # app.add_url_rule(rota, **options)

adicionar_rotas(todas_as_rotas)

if __name__ == '__main__':
    app.run(debug=True)
