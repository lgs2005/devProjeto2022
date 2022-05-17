$(document).ready(() => {
    function pegarValores() {
        return (
            $('#input-nome').val(),
            $('#input-email').val(),
            $('#input-senha').val()
        );
    }

    function validarDados() {
        let (nome, email, senha) = pegarValores();


        return true;
        // TODO
    }



    $('#botao-login').click(() => {
        if (validarDados()) {

        }

        let (nome, email, senha) = pegarValores();
    });

    $('#botao-registro').click(() => {
        if (validarDados()) {

        }
    });
})