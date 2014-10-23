console.log("Cargado... Clase")
$(document).ready(function(){
	cargarOpcionClase()
});

function cargarOpcionClase(e){
	$('.index_clase a').each(function() {
		var $href = $(this).attr('href');
		$(this).on('click', function(e) {
			e.preventDefault()
			e.stopPropagation()
			$('.index_clase a').removeClass('activo')
			$(this).addClass('activo')
			$('#contenedor_clase').load($href);
		});
	})
}