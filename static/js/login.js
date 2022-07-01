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

/**
 * @param {string[]} campos
 */
function pegarValores(...campos) {
	return campos.map((id) => $(id).val())
}

/**
 * @param {string} campo
 * @param {string} erro
 */
function mostrarErro(campo, erro) {
	$(campo).toggleClass("is-invalid", true)
	$(campo + "-erro").text(erro)
}

/**
 * @param {string} campo
 * @param {() => string | undefined} teste
 */
function testarPara(campo, teste) {
	erro = teste();
	if (erro != undefined) {
		mostrarErro(campo, erro)
		return true
	} else {
		return false
	}
}

/**
 * @param {string[]} campos
 */
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

$(function() {

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
			fazerLogin(email, senha)
			.done((resultado) => {
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
			})
			.fail((sts, erro) => {
				console.log("Erro ao fazer login: " + erro)
				mostrarErro(campos.email, "Ocorreu um erro ao fazer login, tente novamente mais tarde.")
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
			fazerRegistro(email, senha, nome)
			
				.done((resultado) => {
					if (resultado.sucesso) {
						location.pathname = '/'
					} else {
						mostrarErro(campos.email, resultado.erro)
					}
				})

				.fail((sts, erro) => {
					console.log("Erro ao fazer registro: " + erro)
					mostrarErro(campos.email, "Ocorreu um erro ao fazer registro, tente novamente mais tarde.")
				})
		}
	})
})
