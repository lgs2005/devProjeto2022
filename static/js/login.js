$(function() {
	// https://www.w3resource.com/javascript/form/email-validation.php
	const emailPattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	const limparErrosDe = [
		"#login-email",
		"#login-senha",
		"#registro-nome",
		"#registro-email",
		"#registro-senha",
	]

	for (let id of limparErrosDe) {
		$(id).on("input", () => {
			$(id).removeClass("is-invalid");
		});
	}

	$("#submit-login").on("click", () => {
		let email = $("#login-email").val().toString();
		let senha = $("#login-senha").val().toString();
		let error = $("#container-erros-email");

		if (email == "") {
			error.text("Preencha o campo email.");
			$("#login-email").addClass("is-invalid");
			console.log("Email vazio.");
		} else if (!emailPattern.test(email)) {
			console.log("Email inválido.");
		} else if (senha == "") {
			console.log("Digite uma senha.");
		} else {
			// fazer o login aqui ?
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
						location.pathname = '/inicio'
					} else {
						console.log(resultado.erro);
					}
				},

				error: () => {
					console.log("Não foi possível fazer login, tente novamente mais tarde.");
				}
			});
		}
	})

	$("#submit-registro").on("click", () => {
		let email = $("#registro-email").val().toString();
		let senha = $("#registro-senha").val().toString();
		let nome = $("#registro-nome").val().toString(); // POR QUE QUE ESSE TEM QUE ESTAR MAIS PRA TRAS EU NAO AGUENTO ISSO POR FVOR

		console.log("registro", email, senha, nome);

		if (email == "")
			console.log("Digite um email."); // cada um desses devia mostrar um erro
		else if (!emailPattern.test(email))
			console.log("Email inválido.");
		else if (senha == "")
			console.log("Digite uma senha.");
		else if (nome == "")
			console.log("Digite seu nome.");
		else {
			// fazer o registro aqui ????
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
						location.pathname = '/inicio'
					} else {
						console.log(resultado.erro);
					}
				},

				error: () => {
					console.log("Não foi possível fazer registro, tente novamente mais tarde.");
				}
			});
		}
	})
})