$(function () { // quando o documento estiver pronto/carregado

    $.ajax({
        url: 'listar_paginas', // qual url????
        method: 'GET',
        dataType: 'json', // os dados são recebidos no formato json
        success: listar_paginas, // chama a função listar para processar o resultado
        error: function () {
            alert("Erro ao ler dados, verifique o backend");
        }
    });

    /** @param {Array} paginas */
    function listar_paginas(paginas) {
        let favoritos = []
        let outras = []

        for (var pagina of paginas) {
            if (pagina.favorito) {
                favoritos.push(pagina)
            }
            else {
                outras.push(pagina)
            }
        }

        listar_paginas(privadas, "#corpoTabelaPaginasPrivadas")
        listar_paginas(outras, "#corpoTabelaOutrasPaginas")
    }

    function listar_paginas(paginas, idLista) {
        for (var pagina of paginas) {
            lin = `<tr><td>${pagina.nome}</td></tr>`;
            $(idLista).append(lin);
        }
    }
});
