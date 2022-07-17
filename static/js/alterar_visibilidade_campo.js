jQuery(function($) {
	$(".visibility-toggle").on("click", function() {
		let buttonId = $(this).attr('id');	
		let inputIcon = $(this).find(".visibility-toggle-icon");
		let input = $(`#${buttonId.replace('-input', '')}`);
		
		// ...
		// sem palavras
		input.attr('type') === 'text'?
			(
				inputIcon.attr("xlink:href", "#eye-slash-fill"),
				input.attr('type', 'password')
			)
			:
			(
				inputIcon.attr("xlink:href", "#eye-fill"),
				input.attr('type', 'text')
			)
	});
})