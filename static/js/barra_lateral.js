$(function () {

    $.ajax({
        url: '/listar_paginas',
        method: 'GET',
        dataType: 'json',
        success: createPagesList,
        error: function () {
            alert("Erro ao ler dados, verifique o backend");
        }
    });
    
    function createPagesList(paginas) {
        for (let pagina of paginas) {
            lin = `<li class="mb-2">${pagina.nome}</li>`;
            
            if (pagina.favorito) {
                $("#listaPaginasFavoritas").append(lin);
            } else {
                $("#listaPaginasComuns").append(lin);
            }
        }
    }
});
