from flask import redirect, render_template

from init import app, db
from login import rota_login, rota_registro, usuario_logado
from pagina import rota_retornar_conteudo


@app.route('/hello')
def hello_world():
    # https://www.youtube.com/watch?v=dwDns8x3Jb4
    return "<img src='https://media1.giphy.com/media/mf8UbIDew7e8g/200.gif'/>" + \
        " ".join(["<p>around the world</p>"] * 144)

def rota_inicio():
    if not usuario_logado():
        return redirect('/login')

    return render_template('inicio.html')

db.create_all()

rotas_simples = {
    '/': rota_inicio,
    '/inicio': rota_inicio,
    '/registrar': rota_registro,
    '/login': rota_login,
    '/retornar_conteudo/<id>': rota_retornar_conteudo,
}

for rota, view in rotas_simples.items():
    app.add_url_rule(rota, view_func=view)
