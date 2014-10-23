console.log("Cargado... Alumno")
$(document).ready(function(){
	cargarOpcionAlumno()
});

function cargarOpcionAlumno(e){
	$('.index_alumno a').each(function() {
		var $href = $(this).attr('href');
		$(this).on('click', function(e) {
			e.preventDefault()
			e.stopPropagation()
			$('.index_alumno a').removeClass('activo')
			$(this).addClass('activo')
			$('#contenedor_alumno').load($href)
		});
	})
}