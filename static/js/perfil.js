$(function () {
    $.ajax({
        url: "/retornar_usuario",
        method: "post",
        dataType: "json",
        success: function(data) {
            $("#id").text(data["id"]);
            $("#nome").text(data["nome"]);
            $("#email").text(data["email"]);
        }
    });
});