from http.client import BAD_REQUEST
from operator import itemgetter
from typing import Any, TypeVar

from flask import abort, jsonify, request

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


T = TypeVar('T')
def get_campos(tipo: 'type[T]', *campos: str) -> 'tuple[T, ...]':
	'''Retorna os valores em campos como uma tuple, verificando que tem o tipo correto
	Para uso em view functions. Causa BAD REQUEST se os campos não estiverem corretos'''

	dados = request.get_json()

	if isinstance(dados, dict):
		abort(BAD_REQUEST)

	for campo in campos:
		if (campo not in dados) or (type(dados[campo]) != tipo):
			abort(BAD_REQUEST)
	
	return itemgetter(*campos)(dados)


def res_ok(value):
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


def res_err(error):
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