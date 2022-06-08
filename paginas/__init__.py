from os.path import dirname
from typing import Union
from uuid import uuid4


THIS_DIR = dirname(__file__)


def caminho_para_pagina(nome: str) -> str:
    return f"{THIS_DIR}/{nome}.json"

def reservar_arquivo() -> Union[str, None]:
    while True:
        id = uuid4().hex
        caminho = caminho_para_pagina(id)
        
        try:
            pagina = open(caminho, 'x')
            pagina.write("{\n}")
            pagina.close()

            return caminho
        except FileExistsError:
            continue
        except OSError:
            return None