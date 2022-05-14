from http.client import UNAUTHORIZED

from flask import abort
from flask_login import current_user
from modelos import Usuario


def requerir_usuario() -> Usuario:
    if not current_user.is_authenticated:
        abort(UNAUTHORIZED, 'Faça login para usar esta rota.')

    return current_user