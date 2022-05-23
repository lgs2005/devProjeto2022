import rotas.conteudo
import rotas.listar_paginas
import rotas.usuario
import rotas.inicio


ROTAS = {
    **rotas.usuario.adicionar_rotas(),
    **rotas.conteudo.adicionar_rotas(),
    **rotas.listar_paginas.adicionar_rotas(),
    **rotas.inicio.adicionar_rotas()
}