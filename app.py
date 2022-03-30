from flask import redirect, render_template

from init import app
from login import usuario_logado


@app.route('/hello')
def hello_world():
    # https://www.youtube.com/watch?v=dwDns8x3Jb4
    return "<img src='https://media1.giphy.com/media/mf8UbIDew7e8g/200.gif'/>" + \
        " ".join(["<p>around the world</p>"] * 200)

@app.route('/')
@app.route('/inicio')
def inicio():
    if not usuario_logado():
        return redirect('/login')

    return render_template('inicio.html')
