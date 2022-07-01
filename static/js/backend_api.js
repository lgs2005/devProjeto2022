/**
 * @param {string} email
 * @param {string} senha
 */
function fazerLogin(email, senha) {
	return $.ajax({
		url: "/api/login",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify({
			email: email,
			senha: senha,
		}),
	})
}

/**
 * @param {string} email
 * @param {string} senha
 * @param {string} nome
 */
function fazerRegistro(email, senha, nome) {
	return $.ajax({
		url: "/api/login",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify({
			email: email,
			senha: senha,
			nome: nome,
			registro: true,
		}),
	})
}