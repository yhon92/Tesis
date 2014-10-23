console.log("Cargado... Profesor")
$(document).ready(function(){
	cargarOpcionPofesor()
});

function cargarOpcionPofesor(e){
	$('.index_profesor a').each(function() {
		var $href = $(this).attr('href');
		$(this).on('click', function(e) {
			e.preventDefault()
			e.stopPropagation()
			$('.index_profesor a').removeClass('activo')
			$(this).addClass('activo')
			$('#contenedor_profesor').load($href);
		});
	})
}