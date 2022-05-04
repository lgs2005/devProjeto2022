import api.conteudo
import api.listar_paginas

ROTAS = {
    **api.conteudo.adicionar_rotas(),
    **api.listar_paginas.adicionar_rotas()
}