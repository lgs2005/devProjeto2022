from init import app, db
from flask import send_from_directory, request

import modelos

import rotas.conteudo
import rotas.auth


@app.route('/', methods=['GET'])
def rota_react():
	'''
	Rota compartilhada com ReactJS.
	./static/index.html
	'''
	return send_from_directory('static', 'index.html')

@app.after_request
def allow_authorization_cors(request):
    request.headers.add('Access-Control-Allow-Headers', 'Authorization')
    return request

if __name__ == '__main__':
    db.create_all()
