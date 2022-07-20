const camposForm = {
	senha: "#alterar-senha-atual",
	novaSenha: "#senha-nova",
}

jQuery(function($) {
	aplicarLimpaDeErros()
	
	$("#submit-alterar").on("click", function() {
		let [senha, novaSenha] = pegarValores(camposForm.senha, camposForm.novaSenha);

		let houveErro = !camposPreenchidos(camposForm.senha, camposForm.novaSenha)
		|| testarPara(camposForm.novaSenha, () => {
			if (novaSenha == senha)
				return "As senhas não podem ser as mesmas";
		});

		if (!houveErro) {
			$.ajax({
				url: "/api/alterar-senha",
				method: "POST",

				contentType: "application/json",
				data: JSON.stringify({
					"senha": senha,
					"novaSenha": novaSenha,
				}),
				
				dataType: "json",
				success: (resultado) => {
					if (resultado.ok) {
						// TODO: mostrar algo dizendo que a senha foi alterada
						// fds vai de alert msm
						alert("Senha alterada.");
					} else {
						mostrarErro(camposForm[resultado.errtarget], resultado.erro);
					};
				},

				error: () => {
					mostrarErro(camposForm.senha, "Ocorreu um erro. Tente novamente mais tarde.")
				}
			});
		}
	});
})
