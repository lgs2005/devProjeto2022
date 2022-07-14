const campos = {
	senha: "#alterar-senha",
	senhaAntiga: "#alterar-senha-antiga",
}

jQuery(function($) {
	aplicarLimpaDeErros()

	$("#submit-password").on("click", function() {
		let [senha, senhaAntiga] = pegarValores(campos.senha, campos.senhaAntiga);

		let houveErro = !camposPreenchidos(campos.senha, campos.senhaAntiga)
		|| testarPara(campos.senha, () => {
			if (senha == senhaAntiga)
				return "Não pode ser a mesma senha.";
		});

		if (!houveErro) {
			$.ajax({
				url: "/api/alterar-senha",
				method: "POST",

				contentType: "application/json",
				data: JSON.stringify({
                    "senha_antiga": senhaAntiga,
					"senha": senha,
				}),
                
				dataType: "json",
				success: (resultado) => {
					console.log(resultado)
					if (resultado.ok) {
                        alert("senha alterada")
                    }
                    else {
                        mostrarErro(campos.senhaAntiga, "Senha incorreta.");
                    }

				},

				error: () => {
					alert("Ocorreu um erro, verifique o backend!")
				}
			});
		}
    })
})
