jQuery(function($) {
    function listItemWrapper(pagina) {
        let listItem = `<a href="#" class="botao-pagina list-group-item list-group-item-action" 
            data-id-pagina="${pagina.id}">${pagina.nome}</a>`;
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
                success: () => recarregarPaginas(),

                error: function() {
                    alert('erro')
                    // animação RIVE de um bonequinho
                }
            })
        }
    });


    $(document).on('click', '.botao-pagina', function() {
        $.ajax({
            url: `api/conteudo/${$(this).attr('data-id-pagina')}`,
            method: 'GET',

            dataType: 'json',
            success:  (pagina) => {
                /** @type {string} */
                let conteudo = pagina.conteudo
                conteudo = conteudo
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
                
                let titulo = pagina.titulo
                titulo = titulo
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');

                let tituloHTML = DOMPurify.sanitize(marked.parse(titulo), {USE_PROFILES: {html: true}})
                $('.titulo-pagina').html(tituloHTML)

                let conteudoHTML = DOMPurify.sanitize(marked.parse(conteudo), {USE_PROFILES: {html: true}})
                $('.conteudo-pagina').html(conteudoHTML)
            },

            error: function() {
                // animação RIVE de um bonequinho
            }
        })
    })  
});
