import json

from os.path import dirname

from typing import Union

from uuid import uuid4


THIS_DIR = dirname(__file__)

def caminho_para_pagina(id: str) -> str:
	'''
	Cria um caminho absoluto para a página
	no formato `[PATH]/[identificação].json`

	Args:
		id (str): identificação hexadecimal.

	Returns:
		str: Caminho absoluto para a página criada.
	'''
	return f"{THIS_DIR}/{id}.json"


def criar_arquivo_pagina(titulo: str = "Sem título") -> Union[str, None]:
	'''
	Cria uma página em json.
	A identificação de cada página no diretório 
	`páginas` é feita com código hexadecimal.

	Returns:
		None: Se acontecer OSError.
		str: Caminho absoluto para a página criada.
	'''
	while True:
		id = uuid4().hex
		caminho = caminho_para_pagina(id)
		
		try:
			pagina = open(caminho, 'x')
			markdown = json.dumps({
				"markdown": {
					"titulo": titulo,
					"conteudo": "escreva aqui" 
				}
			})
			pagina.write(markdown)
			pagina.close()

			return id
		except FileExistsError:
			continue
		except OSError: 
			return None