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
        let [ nomePagina ] = pegarValores('#nome-pagina');
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
        let idPagina = $(this).attr("data-id-pagina");
		let editor = $("#editor");
		let preview = $("#preview");
		let tituloHeader = $("#titulo-pagina");
		let botaoSalvar = $("#botao-salvar-edicoes");
		let botaoVoltar = $("#botao-voltar-edicoes");
		let statusSalvar = $("#status-salvar");
		
		console.log(editor)

		let titulo = "";
		let hasChanges = false;

		function safeMarkdown(markdown) {
			let escapedText = markdown
				.replace(/&/g, "&amp;")
				.replace(/</g, "&lt;")
				.replace(/>/g, "&gt;")
		
			let html = marked.parse(escapedText);
			return DOMPurify.sanitize(html, { USE_PROFILES: { html: true } })
		}	
		
		function updatePreview() {
			tituloHeader.text(titulo)
			preview.html(safeMarkdown($(editor).val()));
		}
	
		editor.on("input", function () {
			hasChanges = true;
		});
	
		botaoVoltar.on("click", function () {
			postChanges()
				.then(() => location.pathname = "/");
		});
	
		botaoSalvar.on("click", function () {
			postChanges();
		})
	
		setInterval(() => {
			if (hasChanges) {
				updatePreview();
				hasChanges = false;
			}
		}, 1000);

		function postChanges() {
			statusSalvar.removeClass("fst-italic").text("Salvando...");
			let conteudo = editor.val();
	
			return $.ajax({
				method: "PUT",
				url: "/api/conteudo/" + idPagina,
	
				contentType: "application/json",
				data: JSON.stringify({
					markdown: {
						titulo: titulo,
						conteudo: conteudo,
					}
				}),
			})
				.then(() => {
					statusSalvar.addClass("fst-italic").text("Mudanças salvas.");
				});
		}

        $.ajax({
			method: "GET",
			url: "/api/conteudo/" + idPagina,
	
			dataType: "json",
			success: (pagina) => {
				titulo = pagina.markdown.titulo;
				editor.val(pagina.markdown.conteudo);
				updatePreview();
			},
	
			error: () => {
				alert("Erro");
			}
		})
    });

    $("#botao-excluir-pagina").on("click", function() {
        $.ajax({
            url: "api/excluir/pagina/" + paginaSelecionada,
            method: 'DELETE',

            success:  () => {
                recarregarPaginas()
            },

            error: function() {
                alert("Não foi possível excluir a página.")
            }
        })
    });
});