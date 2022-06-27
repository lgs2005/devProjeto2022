$(function () {
    let userid = $("#perfil-usuario").attr("data-usuario-id")

    $.ajax({
        url: "/api/perfil/" + userid,
        method: "POST",

        dataType: "application/json",
        success: function(dados) {
            $("#id").text(dados.id);
            $("#nome").text(dados.nome);
            $("#email").text(dados.email);
        },

        error: function(err, errstr) {
            // TODO: avisar erro ao usuario
        }
    });
});