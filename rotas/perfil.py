from http.client import NOT_FOUND

from flask import abort, jsonify, redirect, render_template
from flask_login import current_user
from init import app
from modelos import Usuario

from rotas.utils import pagina_requer_login

# perfil -> outros usuários
# conta -> sua conta


@app.route("/perfil/<int:user_id>", methods=["GET"])
@pagina_requer_login
def rota_perfil_usuario(user_id=None):
    """
    Rota serve a página do usuário caso esteja logado
    """
    return render_template('perfil.html', user_id=user_id)


@app.route("/perfil", methods=["GET"])
@pagina_requer_login
def rota_perfil_default():
    return redirect(f'/perfil/{current_user.id}')


@app.route("/api/perfil/<int:user_id>", methods=["GET"])
def rota_api_perfil_usuario(user_id=None):
    """
    Retorna o JSON de um usuário de acordo com o email

    TODO:
    Talvez seja uma boa ideia verificar se o usuário está logado
    no sistema ou não.
    """
    usuario: Usuario = Usuario.query.filter_by(id=user_id).first()

    if usuario == None:
        abort(NOT_FOUND)
    else:
        return jsonify(usuario.json())


# código do jota
# 2022-2022 você não será esquecido
# def rota_retornar_usuario():
#     """
#     Retorna o JSON de um usuário de acordo com o email

#     TODO:
#     Talvez seja uma boa ideia verificar se o usuário está logado
#     no sistema ou não.
#     """

#     #HARD CODE
#     email = "teste@gmail.com"
#     user : Usuario = Usuario.query.filter_by(email=email).first()
#     u_json = user.json()
#     return jsonify(u_json)
