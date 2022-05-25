$(document).ready(function() {
    for (let controller of $(".slider-control")) {
        let buttons = $(controller).find(".slider-button");
        let faker = $(controller).find(".slider-faker")[0];

        if (buttons.length() < 1 )
            console.error("faltam botões no slider");
        else if (faker == undefined)
            console.error("falt o coisa la");
        else {
            for (let i in buttons) {
                let button = buttons[i];

                button.click(function() {
                    faker.css("transform", scaleX(i))
                });
            }
        }
    }
})