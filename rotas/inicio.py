from flask import redirect, render_template
from flask_login import current_user
from init import app


@app.route("/", methods=["GET"])
def rota_default():
    """
    Rota default, usuário deve estar autenticado, senão
    é redirecionado para `/login`
    """
    return render_template('barra_lateral.html') if current_user.is_authenticated else redirect('/login')
