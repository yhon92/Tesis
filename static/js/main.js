// jQuery.each( [ "put", "delete" ], function( i, method ) {
//   jQuery[ method ] = function( url, data, callback, type ) {
//     if ( jQuery.isFunction( data ) ) {
//       type = type || callback;
//       callback = data;
//       data = undefined;
//     }
 
//     return jQuery.ajax({
//       url: url,
//       type: method,
//       dataType: type,
//       data: data,
//       success: callback
//     });
//   };
// });

$(document).on('ready', function() {
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken')); // Extrae el CSRF Token desde la cookie
				// xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val()); // Extrae el CSRF Token desde un input
			}
		}
	});
	console.log('Cargo Main')
});

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}