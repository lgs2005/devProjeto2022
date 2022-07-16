const camposForm = {
	senhaAtual: "#alterar-senha-atual",
	senha: "#senha-nova",
}

jQuery(function($) {
	aplicarLimpaDeErros()
	
	$("#submit-alterar").on("click", function() {
		let [senha, senhaAtual] = pegarValores(camposForm.senha, camposForm.senhaAtual);

		let houveErro = !camposPreenchidos(camposForm.senha, camposForm.senhaAtual)
		|| testarPara(camposForm.senha, () => {
			if (senha == senhaAtual)
				return "As senhas não podem ser as mesmas";
		});

		if (!houveErro) {
			$.ajax({
				url: "/api/alterar-senha",
				method: "POST",

				contentType: "application/json",
				data: JSON.stringify({
					"senha_antiga": senhaAtual,
					"senha": senha,
				}),
				
				dataType: "json",
				success: (resultado) => {
					if (resultado.ok) {
						location.pathname = '/'
					} else {
						mostrarErro(camposForm.senhaAtual, "Senha incorreta");
					};
				},

				error: () => {
					alert('erro')
				}
			});
		}
	});
})
