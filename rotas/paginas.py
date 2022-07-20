from flask import redirect, render_template
from flask_login import current_user
from init import app


@app.route("/", methods=["GET"])
def rota_default():
    """
    Rota default, usuário deve estar autenticado, senão
    é redirecionado para `/login`
    """
    if current_user.is_authenticated:
        return render_template('inicio.html', user=current_user)
    else:
        return redirect('/login')

@app.route("/editar/<int:id>", methods=["GET"])
def rota_editar(id:int=None):
    return render_template("editar.html", pagina_id=id)