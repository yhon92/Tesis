$(document).ready(identificarUbicacion);

function identificarUbicacion () {
	var pathurl = window.location.pathname
	$('nav ul li a').each(function() {
		var $href = $(this).attr('href')
		if ($href == pathurl){
			$(this).addClass('activo')
		}
	});
}