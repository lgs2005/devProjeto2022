import re

from http.client import BAD_REQUEST

from operator import itemgetter

from typing import Any, TypeVar

from flask import abort, jsonify, request


EMAIL_PATTERN = re.compile(
	"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")

T = TypeVar('T')

def get_campos(tipo: 'type[T]', *campos: str) -> 'tuple[T, ...]':
	'''
	Retorna os valores em campos como uma tuple,
	verificando que tem o tipo correto
	Para uso em view functions. 
	
	Returns:
		200 - BAD REQUEST: Campos incorretos.
	'''
	dados = request.get_json()

	if not isinstance(dados, dict):
		abort(BAD_REQUEST)

	for campo in campos:
		if (campo not in dados) or (type(dados[campo]) != tipo):
			abort(BAD_REQUEST)
	
	return itemgetter(*campos)(dados)


def email_valido(email: str):
	if not EMAIL_PATTERN.fullmatch(email):
		return False


def res_ok(value):
	'''
	Resposta padrão OK.

	Args:
		value: mensagem de resposta.

	Returns:
		Objeto JSON, contento:
		{
			'ok': True,
			'value': mensagem
		}.
	'''
	return jsonify({
		'ok': True,
		'value': value,
	})


def res_err(error):
	'''
	Resposta padrão NÃO OK.

	Args:
		value: mensagem de resposta.

	Returns:
		Objeto JSON, contento:
		{
			'ok': False,
			'value': mensagem
		}.
	'''
	return jsonify({
		'ok': False,
		'error': error,
	})