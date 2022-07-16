from flask import render_template
from flask_login import current_user
from init import app

from rotas.utils import pagina_requer_login


@app.route("/perfil", methods=["GET"])
@pagina_requer_login
def rota_perfil_usuario():
    """
    Rota serve a página do usuário caso esteja logado
    """
    return render_template('perfil.html', user=current_user)