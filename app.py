from flask import redirect, render_template

from init import app, db
from login import view_login, view_registrar, usuario_logado


@app.route('/hello')
def hello_world():
    # https://www.youtube.com/watch?v=dwDns8x3Jb4
    return "<img src='https://media1.giphy.com/media/mf8UbIDew7e8g/200.gif'/>" + \
        " ".join(["<p>around the world</p>"] * 144)

def view_inicio():
    if not usuario_logado():
        return redirect('/login')

    return render_template('inicio.html')

db.create_all()

app.add_url_rule('/', view_func=view_inicio)
app.add_url_rule('/inicio', view_func=view_inicio)

app.add_url_rule('/registrar', view_func=view_registrar)
app.add_url_rule('/login', view_func=view_login)
