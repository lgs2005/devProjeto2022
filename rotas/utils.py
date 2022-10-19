from http.client import BAD_REQUEST
from operator import itemgetter
from typing import Any, TypeVar

from flask import abort, jsonify, request

FieldsType = TypeVar('FieldsType')

def get_json_fields(typing: type[FieldsType], *fields: str) -> tuple[FieldsType, ...]:
	json = request.get_json()

	if not isinstance(json, dict):
		abort(BAD_REQUEST)

	for field in fields:
		if (field not in json) or (type(json[field]) != typing):
			abort(BAD_REQUEST)
	
	return itemgetter(*fields)(json)

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