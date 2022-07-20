let paginaSelecionada = 0

jQuery(function($) {
    function listItemWrapper(pagina) {
        let listItem = `<a href="#" class="botao-pagina list-group-item list-group-item-action" 
            data-id-pagina="${pagina.id}"><span class="overflow-ellipsis">${pagina.nome}</span></a>`;
        return listItem;
    }

    function recarregarPaginas() {
        $.ajax({
            url: '/api/listar-paginas',
            method: 'GET',

            dataType: 'json',
            success: (paginas) => {
                let listas = [
                    '#listaPaginasFavoritas',
                    '#listaPaginasComuns',
                    '#listaPaginasPrivadas',
                ];

                for (let idLista of listas) {
                    $(idLista).children().remove()
                };

                for (let pagina of paginas) {            
                    if (pagina.favorito) {
                        $('#listaPaginasFavoritas').append(listItemWrapper(pagina));
                    } else {
                        $('#listaPaginasComuns').append(listItemWrapper(pagina));
                    };
                };
            },

            error: () => {
                alert('Erro ao ler dados, verifique o backend');
            }
        })
    }

    aplicarLimpaDeErros()
    recarregarPaginas();

    $('#submit-criar-pagina').on('click', function() {
        let [nomePagina] = pegarValores('#nome-pagina');
        let houveErro = !camposPreenchidos('#nome-pagina');

        if (!houveErro) {
            $.ajax({
                url: 'api/criar-pagina',
                method: 'POST',

                contentType: 'application/json',
                data: JSON.stringify({
                    'nome': nomePagina,
                }),

                dataType: 'json',
                success: function() {
                    recarregarPaginas();
                    $("#exampleModal").modal('hide');
                },

                error: function() {
                    mostrarErro("#nome-pagina", "Não foi possível criar a página.");
                    // animação RIVE de um bonequinho
                }
            })
        }
    });

    function safeMarkdown(markdown) {
        let escapedText = markdown
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
        
        let html = marked.parse(escapedText);
        return DOMPurify.sanitize(html, {USE_PROFILES: {html: true}})
    }

    $(document).on('click', '.botao-pagina', function() {
        let idPagina = $(this).attr("data-id-pagina")

        $.ajax({
            url: `api/conteudo/${idPagina}`,
            method: 'GET',

            dataType: 'json',
            success:  (pagina) => {
                paginaSelecionada = idPagina;
                $("#conteudo-principal").removeClass("invisible")
                $('#titulo-pagina').text(pagina.markdown.titulo);
                $('.conteudo-pagina').html(safeMarkdown(pagina.markdown.conteudo))
            },

            error: function() {
                // animação RIVE de um bonequinho
            }
        })
    });

    $("#botao-editar-pagina").on("click", function() {
        console.log(paginaSelecionada)
        location.pathname = "/editar/" + paginaSelecionada;
    });
});
