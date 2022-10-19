from http.client import BAD_REQUEST
from operator import itemgetter
from typing import Any, TypeVar

from flask import abort, jsonify, request


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