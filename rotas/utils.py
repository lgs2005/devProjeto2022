from http.client import BAD_REQUEST, UNAUTHORIZED

from flask import abort, jsonify


def validar_objeto(dados: any, validar: 'dict[str, type]') -> 'dict[str, any]':
    """Recebe dados em json (dict) e dicionário 
    com chaves que devem estar contidas nos dados,
    realizando a verificação necessária.

    Args:
        dados (any): dados json do front-end.
        validar (dict[str, type]): dados que devem estar presentes em dados.

    Returns:
        BAD REQUEST (cod. 400): inválido.
        dados (any): válido.
    """

    if type(dados) != dict:
        abort(BAD_REQUEST)

    for campo in validar:
        if (campo not in dados) or (type(dados[campo]) != validar[campo]):
            abort(BAD_REQUEST)

    return dados

def response_ok(value):
    return jsonify({
        'ok': True,
        'value': value,
    })

def response_err(error):
    return jsonify({
        'ok': False,
        'error': error,
    })