from http.client import BAD_REQUEST
from typing import Any

from flask import abort, jsonify

def validar_dados(dados: any, schema: 'dict[str, type]') -> 'dict[str, Any]':
    """Recebe dados em json (dict) e dicionário 
    com chaves que devem estar contidas nos dados,
    realizando a verificação necessária.

    Args:
        dados (any): dados json do front-end.
        validar (dict[str, type]): dados que devem estar presentes em dados.

    Returns:
        BAD REQUEST (cod. 400): dados inválidos.
        dados (any): dados válidos.
    """

    if type(dados) != dict:
        abort(BAD_REQUEST)

    for key in schema:
        if (key not in dados) or (type(dados[key]) != schema[key]):
            abort(BAD_REQUEST)

    return dados

def resok(value):
	'''
	Resposta padrão OK.

	Args: valor de resposta.

	Contendo {
		Returns:
		Objeto JSON.
	'''
	return jsonify({
		'ok': True,
		'value': value,
	})

def reserr(error):
	'''
	Resposta padrão NÃO OK.

	Args: valor de resposta.

	Returns:
		Objeto JSON.
	'''	
	return jsonify({
		'ok': False,
		'error': error,
	})