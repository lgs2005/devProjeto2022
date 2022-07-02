// https://www.w3resource.com/javascript/form/email-validation.php
const emailPattern = /^[a-zA-Z0-9.!#$%&"*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
const camposForm = {
	login: {
		email: "#login-email",
		senha: "#login-senha"
	},
	registro: {
		email: "#registro-email",
		senha: "#registro-senha",
		nome: "#registro-nome"
	}
}

function pegarValores(...campos) {
	return campos.map((id) => $(id).val())
}

function mostrarErro(campo, erro) {
	$(campo).toggleClass("is-invalid", true)
	$(campo + "-erro").text(erro)
}

function testarPara(campo, teste) {
	erro = teste();
	if (erro != undefined) {
		mostrarErro(campo, erro)
		return true
	} else {
		return false
	}
}

function camposPreenchidos(...campos) {
	let preenchidos = true
	for (let campo of campos) {
		if ($(campo).val().toString() == "") {
			mostrarErro(campo, "Preencha o campo.")
			preenchidos = false
		}
	}
	return preenchidos
}

jQuery(function($) {

	$(".form-control").on("input", function() {
		$(this).removeClass("is-invalid");
	});
	
	$("#submit-login").on("click", function() {
		let campos = camposForm.login
		let [email, senha] = pegarValores(campos.email, campos.senha)

		let houveErro = !camposPreenchidos(campos.email, campos.senha)
		|| testarPara(campos.email, () => {
			if (!emailPattern.test(email))
				return "Email inválido"
		});

		if (!houveErro) {
			$.ajax({
				url: "/api/login",
				method: "POST",
				contentType: "application/json",
				data: JSON.stringify({
					email: email,
					senha: senha,
				}),

				dataType: "json",
				success: (resultado) => {
					if (resultado.sucesso) {
						location.pathname = "/"
					} else {
						// deve ter maneira de melhorar isso, mas não to com vontade no momento
						if (resultado.erro == "Senha incorreta.") {
							mostrarErro(campos.senha, resultado.erro)
						} else {
							mostrarErro(campos.email, resultado.erro)
						}
					}
				},

				error: (_status, erro) => {
					console.log("Erro ao fazer login: " + erro)
					mostrarErro(campos.email, "Ocorreu um erro ao fazer login, tente novamente mais tarde.")
				},
			})
		}
	})

	$("#submit-registro").on("click", function() {
		let campos = camposForm.registro
		let [email, senha, nome] = pegarValores(campos.email, campos.senha, campos.nome)	

		let houveErro = !camposPreenchidos(campos.email, campos.senha, campos.nome)
		|| testarPara(campos.email, () => {
			if (!emailPattern.test(email))
				return "Email inválido"
		});

		if (!houveErro) {
			$.ajax({
				url: "/api/login",
				method: "POST",
				contentType: "application/json",
				data: JSON.stringify({
					email: email,
					senha: senha,
					nome: nome,
					registro: true,
				}),

				dataType: "json",
				success: (resultado) => {
					if (resultado.sucesso) {
						location.pathname = '/'
					} else {
						mostrarErro(campos.email, resultado.erro)
					}
				},

				error: (_status, erro) => {
					console.log("Erro ao fazer registro: " + erro)
					mostrarErro(campos.email, "Ocorreu um erro ao fazer registro, tente novamente mais tarde.")
				},
			})
		}
	})
})
