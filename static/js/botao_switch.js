$(function () {
    $("#login-clickable-area").click(function() {
        $("#animated-divider").removeClass("to-rigth").addClass("to-left")
        $("#coluna-form-registrar").addClass("visually-hidden")
        $("#coluna-form-login").removeClass("visually-hidden")
    })

    $("#registrar-clickable-area").click(function() {
        $("#animated-divider").removeClass("to-left").addClass("to-rigth")
        $("#coluna-form-login").addClass("visually-hidden")
        $("#coluna-form-registrar").removeClass("visually-hidden")
    })
});