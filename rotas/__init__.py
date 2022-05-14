import rotas.conteudo
import rotas.listar_paginas
import rotas.login

ROTAS = {
    **rotas.conteudo.adicionar_rotas(),
    **rotas.listar_paginas.adicionar_rotas(),
    **rotas.login.adicionar_rotas(),
}