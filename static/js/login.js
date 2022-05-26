$(function() {
	$("#submit-login").on("click", () => {
		let email = $("#login-email").val();
		let senha = $("#login-senha").val();

		console.log("login", email, senha);
	})

	$("#submit-registro").on("click", () => {
		let email = $("#registro-email").val();
		let senha = $("#registro-senha").val();
		let nome = $("#registro-nome").val(); // POR QUE QUE ESSE TEM QUE ESTAR MAIS PRA TRAS EU NAO AGUENTO ISSO POR FVOR

		console.log("registro", email, senha, nome);
	})
})