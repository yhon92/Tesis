console.log("Cargado... Reportes")
$(document).ready(function(){
	cargarOpcionHorario()
});

function cargarOpcionHorario(e){
	$('.index_reportes a').each(function() {
		var $href = $(this).attr('href');
		$(this).on('click', function(e) {
			e.preventDefault()
			e.stopPropagation()
			$('.index_reportes a').removeClass('activo')
			$(this).addClass('activo')
			$('#contenedor_reportes').load($href);
		});
	})
}