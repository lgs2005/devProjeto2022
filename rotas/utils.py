from http.client import BAD_REQUEST, UNAUTHORIZED

from flask import abort, jsonify


def validate_data(data: any, validate: 'dict[str, type]') -> 'dict[str, any]':
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

    if type(data) != dict:
        abort(BAD_REQUEST)

    for key in validate:
        if (key not in data) or (type(data[key]) != validate[key]):
            abort(BAD_REQUEST)

    return data

def valid_response(value):
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

def invalid_response(error):
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