$(function() {
	function activateIndex(parent, index) {
		$(parent).find(".slider-button").each((_, button) => {
			let buttonIndex = $(button).attr("data-slider-index");
			$(button).toggleClass("sb-active", buttonIndex == index);
		});
		
		let numIndex = parseInt(index);

		$(parent).find(".slider-item").each((_, item) => {
			let itemIndex = $(item).attr("data-slider-index");
			let numItemIndex = parseInt(itemIndex);
			let move = numItemIndex - numIndex;

			$(item)
				.toggleClass("si-move-left", move < 0)
				.toggleClass("si-move-right", move > 0)
				.toggleClass("si-show", move == 0);
		});
	}

	// set --si-index for styling
	$(".slider-item").each((_, item) => {
		let index = $(item).attr("data-slider-index");
		let numIndex = parseInt(index);

		$(item).css("--si-index", numIndex);
	})

	// ativar o index 1 no documento inteiro
	activateIndex(document, 1);

	for (let controller of $(".slider-control")) {
		for (let button of $(controller).find(".slider-button")) {
			$(button).on("click", () => {
				activateIndex(controller, $(button).attr("data-slider-index"));
			});
		}
	}
})