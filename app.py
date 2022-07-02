from rotas import ROTAS
from init import app, db
from werkzeug.exceptions import HTTPException as WerkzeugHTTPException

@app.route('/hello')
def hello_world():
    """Super Mario Rapper"""
    return '<img src=\'https://c.tenor.com/3fnHh1WgOIwAAAAC/rapping-mario-mario.gif\'/>'



@app.errorhandler(WerkzeugHTTPException)
def error_cat(e: WerkzeugHTTPException):
    return f'<img src="https://http.cat/{e.code}"/>', e.code

@app.errorhandler(Exception)
def internal_error_cat(e: Exception):
    print('\n\n')
    print(e)
    print('\n\n')
    return f'<img src="https://http.cat/500"/>', 500

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
