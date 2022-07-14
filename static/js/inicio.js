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
            success:  (conteudo) => {
                /** @type {string} */
                let markdown = conteudo.markdown
                markdown = markdown
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');

                console.log(markdown)

                let conteudohtml = DOMPurify.sanitize(marked.parse(markdown), {USE_PROFILES: {html: true}})
                $('#conteudo-pagina').html(conteudohtml)
            },

            error: function() {
                // animação RIVE de um bonequinho
            }
        })
    })  
});
