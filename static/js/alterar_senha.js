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

		if (senhaAntiga == "") {
			setErro("senha-antiga", "Preencha o campo senha.")
		}

		if (senha == "") {
			setErro("senha", "Preencha o campo nova senha.");
		}
		else if (senha == senhaAntiga) {
			setErro("senha", "Não pode ser a mesma senha.")
		}

		if (!houveErro) {
			$.ajax({
				url: "/api/alterar_senha",
				method: "POST",

				contentType: "application/json",
				data: JSON.stringify({
                    "senha_antiga": senhaAntiga,
					"senha": senha,
				}),
                
				dataType: "json",
				success: (resultado) => {
					if (resultado.ok) {
                        alert("senha alterada")
                    }
                    else {
                        setErro("senha_antiga", "Senha antiga incorreta.");
                    }

				},

				error: () => {
					alert("Ocorreu um erro, verifique o backend!")
				}
			});
		}
    })
})
