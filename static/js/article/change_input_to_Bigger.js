
$(document).ready(function() {
	$("input[type='text_content']").focus(function() {
		$(this).animate({
			"width" : "400px",
			"height" : "70px"
		})
	}).blur(function() {
		$(this).animate({
			"width" : "100px",
			"height" : "30px"
		})
	});
});