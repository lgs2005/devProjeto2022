$(function() {
	// https://www.w3resource.com/javascript/form/email-validation.php
	const emailPattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	
	const removerErros = [
		"#login-email",
		"#login-senha",
		"#registro-nome",
		"#registro-email",
		"#registro-senha",
	]

	for (let field of removerErros) {
		$(field).on("input", () => {
			$(field).removeClass("is-invalid");
		});
	}
	
	function setErro(campo, erro) {
		$(campo + "-erro").text(erro)
		$(campo).toggleClass("is-invalid", true)
	}


	$("#submit-login").on("click", () => {
		let email = $("#login-email").val().toString();
		let senha = $("#login-senha").val().toString();
		let erro = false
		
		function setErro(campo, erro) {
			$("login-" + campo + "-erro").text(erro)
			$(campo).toggleClass("is-invalid", true)
			erro = true
		}

		if (email == "") {
			setErro("email", "Preencha o campo email.");
		} 
		else if (!emailPattern.test(email)) {
			setErro("email", "Email inválido.");
		}
		
		if (senha == "") {
			setErro("senha", "Preencha o campo senha.");
		}
		
		if (!erro) {
			$.ajax({
				url: '/login',
				method: "POST",
				contentType: "application/json",
				data: JSON.stringify({
					'email': email,
					'senha': senha,
				}),

				dataType: "json",
				success: (resultado) => {
					if (resultado.sucesso) {
						// redirecionar para '/inicio'
						location.pathname = '/inicio'
					} else {
						if (resultado.erro == "Senha incorreta.") {
							senhaErro.text(resultado.erro)
							$("#login-senha").addClass("is-invalid");
						} else {
							emailErro.text(resultado.erro)
							$("#login-email").addClass("is-invalid");
						}
					}
				},

				error: () => {
					// ERRO DO SERVIDOR.
				}
			});
		}
	})

	$("#submit-registro").on("click", () => {
		let email = $("#registro-email").val().toString();
		let senha = $("#registro-senha").val().toString();
		let nome = $("#registro-nome").val().toString();
		let erro = false
		
		function setErro(campo, erro) {
			$("registro-" + campo + "-erro").text(erro)
			$(campo).toggleClass("is-invalid", true)
			erro = true
		}

		if (email == "") {
			setErro("email", "Preencha o campo email.");
		}
		else if (!emailPattern.test(email)) {
			setErro("email", "Email inválido.");
		}
		
		if (senha == "") {
			setErro("senha", "Preencha o campo senha.");
		}
		
		if (nome == "") {
			setErro("nome", "Preencha o campo nome.");
		}
		
		if (!erro) {
			$.ajax({
				url: '/registrar',
				method: "POST",
				contentType: "application/json",
				data: JSON.stringify({
					'email': email,
					'senha': senha,
					'nome': nome,
				}),

				dataType: "json",
				success: (resultado) => {
					if (resultado.sucesso) {
						// redirecionar para '/inicio'
						location.pathname = '/inicio'
					} else {
						emailErro.text(resultado.erro)
						$("#registro-email").addClass("is-invalid");
					}
				},

				error: () => {
					// ERRO DO SERVIDOR.
				}
			});
		}
	})
})
