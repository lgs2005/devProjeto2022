$(function () {
    $('.form-control').on('input', function() {
		$(this).removeClass('is-invalid');
	});
    
    $.ajax({
        url: '/listar_paginas',
        method: 'GET',
        dataType: 'json',
        success: function (paginas) {
            if ($.isEmptyObject(paginas)) {
                noPagesYet = `<li class="text-white mt-2">Nenhuma página ainda...</li>`;
                $('#listaPaginasFavoritas').append(noPagesYet);
                $('#listaPaginasComuns').append(noPagesYet);
                $('#listaPaginasPrivadas').append(noPagesYet);
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
        error: function () {
            alert('Erro ao ler dados, verifique o backend');
        }
    });
    
    
    redirecionar_app = function(resultado) {
        if (resultado.sucesso) {
            location.pathname = '/teste_barra_lateral'
        }
    }


    renderizar_pagina = function(pagina) {
        $('.conteudo-principal').removeClass('bg-light').addClass('bg-secondary');
        $('#titulo-pagina').text(pagina.titulo);
        $('#conteudo-pagina').text(pagina.conteudo);
    }

    function redirecionar_pagina(pagina) {

    }


    $(document).on('click', '#submit-criar-pagina', function() {
        let nomePagina = $('#nome-pagina').val().toString();
        let houveErro = false

        function setErro(campo, erro) {
			$(`#nome-${campo}-erro`).text(erro);
			$(`#nome-${campo}`).addClass('is-invalid');
			houveErro = true;
		}

        if (nomePagina == '') {
			setErro('pagina', 'Preencha o campo nome.');
		} 

        if (!houveErro) {
            $.ajax({
                url: 'api/criar_pagina',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    'nome': nomePagina,
                }),

                dataType: 'json',
                success: rediredionar_app,

                error: function() {
                    alert('erro')
                    // animação RIVE de um bonequinho
                }
            })
        }
    })  


    $(document).on('click', '.botao-pagina', function() {
        $.ajax({
            url: `api/conteudo/${parseInt($(this).attr('data-id-pagina'))}`,
            method: 'GET',

            dataType: 'json',
            success:  renderizar_pagina,

            error: function() {
                // animação RIVE de um bonequinho
            }
        })
    })   

});
