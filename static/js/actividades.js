console.log("Cargado... Actividades")
$(document).ready(function(){
	cargarOpcionActividar()
});

function cargarOpcionActividar(e){
	$('.index_actividades a').each(function() {
		var $href = $(this).attr('href');
		$(this).on('click', function(e) {
			e.preventDefault()
			e.stopPropagation()
			$('.index_actividades a').removeClass('activo')
			$(this).addClass('activo')
			$('#contenedor_actividades').load($href);
		});
	})
}