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
        for (var i in paginas) {
            if (paginas[i].favorito) {
                lin = '<li class="mb-2">' + paginas[i].nome + '</li>';
                $("#listaPaginasFavoritas").append(lin);
            } else {
                lin = '<li class="mb-2">' + paginas[i].nome + '</li>';
                $("#listaPaginasComuns").append(lin);
            }
        }
    }
});
