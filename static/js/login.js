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

	$("#submit-login").on("click", () => {
		let email = $("#login-email").val().toString();
		let senha = $("#login-senha").val().toString();

		let emailErro = $("#login-email-erro");
		let senhaErro = $("#login-senha-erro");

		if (email == "") {
			emailErro.text("Preencha o campo email.");
			$("#login-email").addClass("is-invalid");
		} 
		else if (!emailPattern.test(email)) {
			emailErro.text("Email inválido.");
			$("#login-email").addClass("is-invalid");
		} 
		if (senha == "") {
			senhaErro.text("Preencha o campo senha.");
			$("#login-senha").addClass("is-invalid");
		} 
		else {
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

		let emailErro = $("#registro-email-erro");
		let senhaErro = $("#registro-senha-erro");
		let nomeErro = $("#registro-nome-erro");

		if (email == "") {
			emailErro.text("Preencha o campo email.");
			$("#registro-email").addClass("is-invalid");
		}
		else if (!emailPattern.test(email)) {
			emailErro.text("Email inválido.");
			$("#registro-email").addClass("is-invalid");
		}
		if (senha == "") {
			senhaErro.text("Preencha o campo senha.");
			$("#registro-senha").addClass("is-invalid");
		}
		if (nome == "") {
			nomeErro.text("Preencha o campo nome.");
			$("#registro-nome").addClass("is-invalid");
		}
		else {
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