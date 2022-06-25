from functools import wraps
from http.client import BAD_REQUEST, UNAUTHORIZED
from flask import abort
from flask_login import current_user


def requer_login(rota):
    """Checa se o usuário está
    autenticado (login).

    Args:
        rota (function): rota a ser tratada.

    Returns:
        decorador.
    """
    @wraps(rota)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(UNAUTHORIZED)
        
        return rota(*args, **kwargs)

    return wrapper


def validar_objeto(dados: any, validar: 'dict[str, type]') -> 'dict[str, any]':
    """Recebe dados em json (dict) e dicionário com chaves
    que devem estar contidas nos dados.

    Args:
        dados (any): dados json do front-end.
        validar (dict[str, type]): dados que devem estar presentes em <dados>.

    Returns:
        abort(BAD REQUEST - 400): caso inválido.
        dict[str, any]: caso válido.
    """

    if type(dados) != dict:
        abort(BAD_REQUEST)

    for campo in validar:
        if (campo not in dados) or (type(dados[campo]) != validar[campo]):
            abort(BAD_REQUEST)
    
    return dados