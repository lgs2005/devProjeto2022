from http.client import UNAUTHORIZED

from flask import abort
from login import usuario_logado


def requerir_usuario():
    usuario = usuario_logado()
    if usuario == None:
        abort(UNAUTHORIZED, "Usuário não encontrado")
    return usuario
