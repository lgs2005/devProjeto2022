from flask import redirect, render_template

import api
from init import app, db
from login import rota_login, rota_registro, usuario_logado


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


def adicionar_rotas(rotas):
    for rota, options in rotas.items():
        if type(options) == dict:
            app.add_url_rule(rota, **options)
        else:
            app.add_url_rule(rota, view_func=options)


outras_rotas = {
    '/': rota_inicio,
    '/inicio': rota_inicio,
    '/registrar': rota_registro,
    '/login': rota_login,
}

adicionar_rotas(outras_rotas)
adicionar_rotas(api.ROTAS)

if __name__ == '__main__':
    app.run(debug=True)
