$(function() {
    // limpar erros em form
    $('.form-control').on('input', function() {
		$(this).removeClass('is-invalid');
	});

	$("#submit-password").on("click", function() {
        let senhaAntiga = $("#alterar-senha-antiga").val().toString();
		let senha = $("#alterar-senha").val().toString();
		let houveErro = false

		function setErro(campo, erro) {
			$(`#alterar-${campo}-erro`).text(erro);
			$(`#alterar-${campo}`).addClass("is-invalid");
			houveErro = true;
		}

		if (senha == "") {
			setErro("senha", "Preencha o campo senha.");
		} 

		if (!houveErro) {
			$.ajax({
				url: "/alterar_senha",
				method: "POST",
				contentType: "application/json",
				data: JSON.stringify({
                    "senha_antiga": senhaAntiga,
					"senha": senha,
				}),
                
				success: (resultado) => {
                    console.log(resultado)
					if (resultado == "Ok") {
                        alert("senha alterad")
                    }
                    else {
                        alert(resultado)
                        setErro("senha_antiga", "Senha antiga incorreta.");
                    }

				},

				error: () => {
					// ERRO DO SERVIDOR.
				}
			});
		}
    })
})
