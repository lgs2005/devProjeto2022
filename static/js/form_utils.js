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

function aplicarLimpaDeErros() {
    $('.form-control').on('input', function() {
		$(this).removeClass('is-invalid');
	});
}