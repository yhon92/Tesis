function soloLetras(e){
	key = e.keyCode || e.which;
	tecla = String.fromCharCode(key).toLowerCase();
	letras = " áéíóúüabcdefghijklmnñopqrstuvwxyz";
	especiales = [8,37,39,46];
	tecla_especial = false
	for(var i in especiales){
		if(key == especiales[i]){
			tecla_especial = true;
			break;
		}
	}
	if(letras.indexOf(tecla)==-1 && !tecla_especial){
		return false;
	}
}

function soloNum(e){
	key = e.keyCode || e.which;
	tecla = String.fromCharCode(key).toLowerCase();
	num = "0123456789";
	especiales = [8,37,39,46];
	tecla_especial = false
	for(var i in especiales){
		if(key == especiales[i]){
			tecla_especial = true;
			break;
		}
	}
	if(num.indexOf(tecla)==-1 && !tecla_especial){
		return false;
	}
}

function soloBorrar(e){
	key = e.keyCode || e.which;
	tecla = String.fromCharCode(key).toLowerCase();
	num = "";
	especiales = [8,13,];
	tecla_especial = false
	for(var i in especiales){
		if(key == especiales[i]){
			tecla_especial = true;
			break;
		}
	}
	if(num.indexOf(tecla)==-1 && !tecla_especial){
		return false;
	}
}

function ningunaTecla(e){
	return false;
}

// Forma de Uso: onkeyup="format(this)"
function format(input){
	var num = input.value.replace(/\./g,'');
	if(!isNaN(num)){
		num = num.toString().split('').reverse().join('').replace(/(?=\d*\.?)(\d{3})/g,'$1.');
		num = num.split('').reverse().join('').replace(/^[\.]/,'');
		input.value = num;
	}else{
		// alert('Solo se permiten numeros');
		// input.value = input.value.replace(/[^\d\.]*/g,'');
	}
}

function validarCedula (cedula) {
	if (parseInt(cedula) > 0 || cedula == 'Menor'){
		return true
	}
	else{
		alertify.log("¡Cédula Invalida!")
		return false
	}
}

function validarHoras (desde, hasta) {
	desde = moment(desde, 'h:mm a').format('HH:mm')
	hasta = moment(hasta, 'h:mm a').format('HH:mm')
	if (desde > hasta){
		alertify.log("¡Hora Desde es mayor!")
		return false
	}else if (desde == hasta) {
		alertify.log("¡Hora Desde y Hora Hasta son iguales!")
		return false
	}else{
		return true
	}
}

function validarAnioDeNacimiento (fecha) {
	ahora = moment().format('YYYY')
	fecha = moment(fecha, 'DD-MM-YYYY').format('YYYY')
	if ((ahora - fecha) > 2) {
		return true
	}
	else{
		alertify.log("¡Fecha de Nacimiento Invalida!")
		return false
	}
}

function validarString (titulo, string) {
	if(recorrerString(string) == false ) {
			alertify.log('¡Campo '+ titulo +' Invalido!')
			return false
	} else {
		return true
	}
}

function recorrerString(string) {
	for ( i = 0; i < string.length; i++ ) {
		if ( string.charAt(i) != " " ) {
			return true
		}
	}
	return false
}

function compararFechas (desde, hasta) {
	if (Date.parse(reconvertirFecha(desde)) > Date.parse(moment().format('YYYY-MM-DD'))){
		alertify.error("La fecha Desde es mayor que hoy")
		return false
	}else	if (Date.parse(reconvertirFecha(hasta)) > Date.parse(moment().format('YYYY-MM-DD'))){
		alertify.error("La fecha Hasta es mayor que hoy")
		return false
	}else if (Date.parse(reconvertirFecha(desde)) > Date.parse(reconvertirFecha(hasta))) {
		alertify.error("La fecha Desde es mayor que la fecha Hasta")
		return false
	}else {
		return true
	}
}

function reconvertirFecha(fecha) {
	nuevaFecha = moment(fecha, 'DD-MM-YYYY').format('YYYY-MM-DD')
	return nuevaFecha
}

// Forma de Uso: onkeyup="puntoEnMiles(this,this.value.charAt(this.value.length-1));"
/*function puntoEnMiles(donde,caracter){
	pat = /[\*,\+,\(,\),\?,\\,\$,\[,\],\^]/
	valor = donde.value
	largo = valor.length
	crtr = true
	
	if(isNaN(caracter) || pat.test(caracter) == true){
		if (pat.test(caracter)==true){
			caracter = "\\" + caracter
		}
		carcter = new RegExp(caracter,"g")
		valor = valor.replace(carcter,"")
		donde.value = valor
		crtr = false
	}else{
		var nums = new Array()
		cont = 0
		for(m=0;m<largo;m++){
			if(valor.charAt(m) == "." || valor.charAt(m) == " "){continue;}
		else{
			nums[cont] = valor.charAt(m)
			cont++
		}}
	}
	
	var cad1="",cad2="",tres=0
	if(largo > 3 && crtr == true){
		for (k=nums.length-1;k>=0;k--){
			cad1 = nums[k]
			cad2 = cad1 + cad2
			tres++
			if((tres%3) == 0){
				if(k!=0){
					cad2 = "." + cad2
			}}}
		donde.value = cad2
	}
}*/