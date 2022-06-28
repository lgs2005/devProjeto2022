from flask import redirect, render_template, jsonify, abort
from flask_login import current_user
from http.client import NOT_FOUND

from modelos import Usuario
from rotas.utils import pagina_requer_login

# perfil -> outros usuários
# conta -> sua conta
@pagina_requer_login
def rota_perfil_usuario(user_id=None):
    """
    Rota serve a página do usuário caso esteja logado
    """
    return render_template('perfil.html', user_id=user_id)


@pagina_requer_login
def rota_perfil_default():
    return redirect(f'/perfil/{current_user.id}')


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


### código do jota
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

def adicionar_rotas():
    return {
        '/perfil/<int:user_id>': {
            'view_func': rota_perfil_usuario,
            'methods': ["GET"],
        },

        '/perfil': {
            'view_func': rota_perfil_default,
            'methods': ["GET"],
        },

        '/api/perfil/<int:user_id>': {
            'view_func': rota_api_perfil_usuario,
            'methods': ["GET"],
        }
    }