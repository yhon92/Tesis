console.log("Cargado... Horario")
$(document).ready(function(){
	cargarOpcionHorario()
});

function cargarOpcionHorario(e){
	$('.index_horario a').each(function() {
		var $href = $(this).attr('href');
		$(this).on('click', function(e) {
			e.preventDefault()
			e.stopPropagation()
			$('.index_horario a').removeClass('activo')
			$(this).addClass('activo')
			$('#contenedor_horario').load($href);
		});
	})
}