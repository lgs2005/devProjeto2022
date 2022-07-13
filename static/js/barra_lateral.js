jQuery(function($) {
    function recarregarPaginas() {
        $.ajax({
            url: '/api/listar_paginas',
            method: 'GET',

            dataType: 'json',
            success: (paginas) => {
                let listas = [
                    '#listaPaginasFavoritas',
                    '#listaPaginasComuns',
                    '#listaPaginasPrivadas',
                ]

                for (let idLista of listas) {
                    $(idLista).children().remove()
                }

                if ($.isEmptyObject(paginas)) {
                    for (let idLista of listas) {
                        $(idLista).append(`<li class="text-white mt-2">Nenhuma página ainda...</li>`)
                    }
                }
                else {
                    for (let pagina of paginas) {
                        lin = `<li class='mb-2 botao-pagina' data-id-pagina='${pagina.id}'>${pagina.nome}</li>`;
            
                        if (pagina.favorito) {
                            $('#listaPaginasFavoritas').append(lin);
                        } else {
                            $('#listaPaginasComuns').append(lin);
                        }
                    }
                }
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
                url: 'api/criar_pagina',
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
