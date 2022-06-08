from http.client import BAD_REQUEST, UNAUTHORIZED
from flask import abort
from flask_login import current_user


def requer_login(rota):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(UNAUTHORIZED)
        
        return rota(*args, **kwargs)

    return wrapper

def validar_objeto(dados: any, validar: dict[str, type]) -> dict[str, any]:
    if type(dados) != dict:
        abort(BAD_REQUEST)

    for campo in validar:
        if (campo not in dados) or (type(dados[campo]) != validar[campo]):
            abort(BAD_REQUEST)
    
    return dados