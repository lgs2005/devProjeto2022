$(function() {
	// https://www.w3resource.com/javascript/form/email-validation.php
	const emailPattern = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
	
	$(".form-control").on("input", function() {
		$(this).removeClass("is-invalid");
	});
	
	$("#submit-login").on("click", function() {
		let email = $("#login-email").val().toString();
		let senha = $("#login-senha").val().toString();
		let houveErro = false
		
		function setErro(campo, erro) {
			$(`#login-${campo}-erro`).text(erro);
			$(`#login-${campo}`).addClass("is-invalid");
			houveErro = true;
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

		if (!houveErro) {
			$.ajax({
				url: '/api/login',
				method: "POST",
				contentType: "application/json",
				data: JSON.stringify({
					'email': email,
					'senha': senha,
				}),

				dataType: "json",
				success: (resultado) => {
					if (resultado.sucesso) {
						// redirecionar para '/'
						location.pathname = '/'
					} else {
						if (resultado.erro == "Senha incorreta.") {
							setErro("senha", resultado.erro)
						} else {
							setErro("email", resultado.erro)
						}
					}
				},

				error: () => {
					// ERRO DO SERVIDOR.
				}
			});
		}
	})

	$("#submit-registro").on("click", function() {
		let email = $("#registro-email").val().toString();
		let senha = $("#registro-senha").val().toString();
		let nome = $("#registro-nome").val().toString();
		let houveErro = false
		
		function setErro(campo, erro) {
			$(`#registro-${campo}-erro`).text(erro)
			$(`#registro-${campo}`).toggleClass("is-invalid", true)
			houveErro = true
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
		
		if (!houveErro) {
			$.ajax({
				url: '/api/login',
				method: "POST",
				contentType: "application/json",
				data: JSON.stringify({
					'registro': true,
					'email': email,
					'senha': senha,
					'nome': nome,
				}),

				dataType: "json",
				success: (resultado) => {
					if (resultado.sucesso) {
						// redirecionar para '/'
						location.pathname = '/'
					} else {
						setErro("email", resultado.erro)
					}
				},

				error: () => {
					// ERRO DO SERVIDOR.
				}
			});
		}
	})
})
