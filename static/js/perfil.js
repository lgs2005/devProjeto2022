let userid = $(document.currentScript).attr("data-usuario-id")

$(() => {
    $.ajax({
        url: "/api/perfil/" + userid,
        method: "GET",

        dataType: "json",
        success: function (dados) {
            $("#nome").text(dados.nome);
            $("#email").text(dados.email);
        },

        error: function (err, errstr) {
            // TODO: avisar erro ao usuario
            // tbm vai aqui se o usuario não tiver acesso!
        }
    });
});