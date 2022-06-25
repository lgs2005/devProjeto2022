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
            lin = `<li class="mb-2 botao-pagina" data-id-pagina="${pagina.id}">${pagina.nome}</li>`;

            if (pagina.favorito) {
                $("#listaPaginasFavoritas").append(lin);
            } else {
                $("#listaPaginasComuns").append(lin);
            }
        }
    }

    $(document).on("click", ".botao-pagina", function() {
        $.ajax({
            url: `api/conteudo/${parseInt($(this).attr("data-id-pagina"))}`,
            method: 'GET',
            dataType: 'string',
            sucess: renderizarPagina,
            error: function() {
                alert('animação foda')
            }
        })
    })

    function renderizarPagina(pagina) {
        pagina = JSON.parse(pagina);
        console.log(pagina);
    }
});
