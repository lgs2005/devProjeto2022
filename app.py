from init import app, db
from flask import render_template
import json

import modelos

import rotas.conteudo
import rotas.auth
import rotas.share


@app.get('/')
def rota_react():
	'''
	Rota compartilhada com ReactJS.
	./static/index.html
	'''
	return render_template('index.html', extradata=json.dumps({'test': 'hi'}))


if __name__ == '__main__':
	db.create_all()
