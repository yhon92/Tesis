# -- coding: utf-8 --
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from actividades.models import Tipo_Actividad, Actividad
from alumnos.models import Alumno, Prenda, Alumno_Prenda, Alumno_Actividad, Nivel_I, Clase_Individual, Clase_Catedra
from clases.models import Clase, Catedra, Nivel, Seccion
from horarios.models import Horario
from instrumentos.models import Instrumento
from profesores.models import Profesor, Designacion
from .models import Bitacora

@login_required
def index(request):
	template = 'index_reportes.html'
	return render(request, template)

@login_required
def bitacora(request):
	usuarios = User.objects.all()
	modulos = Bitacora.objects.values('modulo').distinct()
	template = 'index_bitacora.html'
	return render(request, template, locals())

@login_required
def cargar_opcion(request):
	instrumentos = Instrumento.objects.order_by('id').all()
	niveles_i = Nivel_I.objects.order_by('id').all()
	actividades = Actividad.objects.order_by('tipo','nombre').all()
	# clases = Clase.objects.order_by('catedra', 'nivel', 'seccion').all()
	catedras = Catedra.objects.order_by('id').all()
	niveles = Nivel.objects.order_by('id').all()
	secciones = Seccion.objects.order_by('id').all()
	template = request.POST['template']
	return render(request, template, locals())


@login_required
def especiales(request):
	template = 'index_especiales.html'
	return render(request, template, locals())


##################################-Para PDF-##################################
import cgi
import ho.pisa as pisa
import cStringIO as StringIO
from django.db import connection
from django.template import RequestContext
from django.template.loader import render_to_string
##################################-Para PDF-##################################
@login_required
def buscar_visualizar_bitacora(request, tipo, usuario, modulo, accion, desde, hasta, funcion):
	sql = 'SELECT u.username, b.modulo, b.fecha, b.accion, b.mensaje FROM reportes_bitacora b, auth_user u WHERE b.usuario_id=u.id'
	sql = sql + ' AND b.fecha BETWEEN "'+ desde +' 00:00:00" AND "'+ hasta +' 23:59:59"'
	if usuario != 'todos':
		sql = sql + ' AND b.usuario_id="'+ usuario +'"'
	if modulo != 'todos':
		sql = sql + ' AND b.modulo="'+ modulo +'"'
	if accion != 'todos':
		sql = sql + ' AND b.accion="'+ accion +'"'
	sql = sql + 'ORDER BY b.fecha'
	
	b = connection.cursor()
	b.execute(sql)
	bitacoras = dictfetchall(b)

	if tipo == 'visualizar':
		template = 'visualizar_bitacora.html'
		return render(request, template, locals())
	
	if bitacoras != []:
		if funcion == 'Comprobar':
			return JsonResponse({'estado': 1})
		elif funcion == 'Imprimir':
			if tipo == 'pdf':
			
				num = 0
				for bitacora in bitacoras:
					num = num + 1
					if num < 10:
						bitacora['num'] = '0' + str(num)
					else:
						bitacora['num'] = str(num)
				# fecha = datetime.date.today()
				desde = datetime.datetime.strptime(desde, '%Y-%m-%d').date()
				hasta = datetime.datetime.strptime(hasta, '%Y-%m-%d').date()
				pagesize = 'Letter'
				html = render_to_string('pdf_bitacora.html', locals(), context_instance=RequestContext(request))
				return generar_pdf(html)
	else:
		return JsonResponse({'estado': 3})

@login_required
def mostrar_fecha(request, fecha, cedula, estado, sexo, desde, hasta, funcion):
	sql = 'SELECT CONCAT(a.nombres ," ", a.apellidos) AS nombre, a.cedula, a.fecha_nacimiento AS fecha, a.sexo, a.activo AS estado FROM alumnos_alumno a WHERE'
	sql = sql + ' a.'+ fecha +' BETWEEN "'+ desde +'" AND "'+ hasta +'"'
	if cedula != 'todos':
		sql = sql + ' AND a.menor = ' + '"'+ cedula +'"'
	if estado != 'todos':
		sql = sql + ' AND a.activo = ' + '"'+ estado +'"'
	if sexo != 'todos':
			sql = sql + ' AND a.sexo = ' + '"'+ sexo +'"'
	sql = sql + ' ORDER BY a.fecha_nacimiento, nombre'

	a = connection.cursor()
	a.execute(sql)
	alumnos = dictfetchall(a)

	if alumnos != []:
		if funcion == 'Comprobar':
			return JsonResponse({'estado': 1})
		elif funcion == 'Imprimir':
			num = 0
			for alumno in alumnos:
				num = num + 1
				if num < 10:
					alumno['num'] = '0' + str(num)
				else:
					alumno['num'] = str(num)
				if alumno['estado'] == 1:
					alumno['estado'] = 'Activo'
				else:
					alumno['estado'] = 'Inactivo'
				alumno['edad'] = calcular_edad(alumno['fecha'])
			desde = datetime.datetime.strptime(desde, '%Y-%m-%d').date()
			hasta = datetime.datetime.strptime(hasta, '%Y-%m-%d').date()
			pagesize = 'Letter'
			html = render_to_string('pdf_fecha.html', locals(), context_instance=RequestContext(request))
			return generar_pdf(html)
	else:
		return JsonResponse({'estado': 3})


@login_required
def mostrar_instrumento(request, instrumento, nivel, cedula, estado, sexo, funcion):
	sql = 'SELECT CONCAT(a.nombres ," ", a.apellidos) AS nombre, a.cedula, a.fecha_nacimiento AS fecha, a.sexo, a.activo AS estado, n.nombre AS nivel, i.nombre AS instrumento FROM alumnos_alumno a, alumnos_clase_individual aci, alumnos_nivel_i n, instrumentos_instrumento i WHERE a.id = aci.alumno_id AND aci.nivel_id = n.id AND aci.instrumento_id = i.id'
	if instrumento != 'todos':
		sql = sql + ' AND aci.instrumento_id = ' + '"'+ instrumento +'"'
		instrumento = Instrumento.objects.get(id=instrumento)
	if nivel != 'todos':
		sql = sql + ' AND n.id = ' + '"'+ nivel +'"'
		nivel = Nivel_I.objects.get(id=nivel)
	if cedula != 'todos':
		sql = sql + ' AND a.menor = ' + '"'+ cedula +'"'
	if estado != 'todos':
		sql = sql + ' AND a.activo = ' + '"'+ estado +'"'
	if sexo != 'todos':
		sql = sql + ' AND a.sexo = ' + '"'+ sexo +'"'
	sql = sql + ' ORDER BY i.orden, n.id, nombre '
		
	a = connection.cursor()
	a.execute(sql)
	alumnos = dictfetchall(a)
	
	if alumnos != []:
		if funcion == 'Comprobar':
			return JsonResponse({'estado': 1})
		elif funcion == 'Imprimir':
			num = 0
			for alumno in alumnos:
				num = num + 1
				if num < 10:
					alumno['num'] = '0' + str(num)
				else:
					alumno['num'] = str(num)
				if alumno['estado'] == 1:
					alumno['estado'] = 'Activo'
				else:
					alumno['estado'] = 'Inactivo'
				alumno['edad'] = calcular_edad(alumno['fecha'])
			pagesize = 'Letter'
			html = render_to_string('pdf_instrumento.html', locals(), context_instance=RequestContext(request))
			return generar_pdf(html)
	else:
		return JsonResponse({'estado': 3})

@login_required
def mostrar_actividad(request, actividad, instrumento, cedula, estado, sexo, funcion):
	sql = 'SELECT CONCAT(al.nombres ," ", al.apellidos) AS nombre, al.cedula, al.fecha_nacimiento AS fecha, al.sexo, al.activo AS estado, CONCAT(i.nombre ," ", aac.clasificacion) AS instrumento FROM actividades_actividad ac, alumnos_alumno_actividad aac, alumnos_alumno al, instrumentos_instrumento i WHERE al.id = aac.alumno_id AND ac.id = aac.actividad_id AND i.id = aac.instrumento_id AND aac.actividad_id = "' + actividad + '"'
	if instrumento != 'todos':
		sql = sql + ' AND aac.instrumento_id = ' + '"'+ instrumento +'"'
	if cedula != 'todos':
		sql = sql + ' AND al.menor = ' + '"'+ cedula +'"'
	if estado != 'todos':
		sql = sql + ' AND al.activo = ' + '"'+ estado +'"'
	if sexo != 'todos':
		sql = sql + ' AND al.sexo = ' + '"'+ sexo +'"'
	sql = sql + ' ORDER BY i.orden, aac.clasificacion, nombre '
	
	a = connection.cursor()
	a.execute(sql)
	alumnos = dictfetchall(a)

	if alumnos != []:
		if funcion == 'Comprobar':
			return JsonResponse({'estado': 1})
		elif funcion == 'Imprimir':
			num = 0
			for alumno in alumnos:
				num = num + 1
				if num < 10:
					alumno['num'] = '0' + str(num)
				else:
					alumno['num'] = str(num)
				if alumno['estado'] == 1:
					alumno['estado'] = 'Activo'
				else:
					alumno['estado'] = 'Inactivo'
				alumno['edad'] = calcular_edad(alumno['fecha'])
			actividad = Actividad.objects.get(id=actividad)
			try:
				director = Designacion.objects.get(actividad_id=actividad, cargo__nombre='Director')
			except Exception:
				pass
			try:
				asistente = Designacion.objects.get(actividad_id=actividad, cargo__nombre='Asistente')
			except Exception:
				pass
			modulo = 'reportes'
			pagesize = 'Letter'
			html = render_to_string('pdf_actividad.html', locals(), context_instance=RequestContext(request))
			return generar_pdf(html)
	else:
		return JsonResponse({'estado': 3})

@login_required
def mostrar_catedra(request, catedra, nivel, seccion, cedula, estado, sexo, funcion):
	sql = 'SELECT CONCAT(a.nombres ," ", a.apellidos) AS nombre, a.cedula, a.fecha_nacimiento AS fecha, a.sexo, a.activo AS estado, n.nombre AS nivel FROM alumnos_alumno a, alumnos_clase_catedra acc, clases_clase cl, clases_nivel n, clases_catedra c, clases_seccion s WHERE a.id = acc.alumno_id AND acc.clase_id = cl.id AND cl.nivel_id = n.id AND cl.catedra_id = c.id AND cl.seccion_id = s.id AND c.id = "' + catedra + '"'
	catedra = Catedra.objects.get(id=catedra)
	if nivel != 'todos':
		sql = sql + ' AND n.id = ' + '"'+ nivel +'"'
		nivel = Nivel.objects.get(id=nivel)
	if seccion != 'todos':
		sql = sql + ' AND s.id = ' + '"'+ seccion +'"'
	if cedula != 'todos':
		sql = sql + ' AND a.menor = ' + '"'+ cedula +'"'
	if estado != 'todos':
		sql = sql + ' AND a.activo = ' + '"'+ estado +'"'
	if sexo != 'todos':
		sql = sql + ' AND a.sexo = ' + '"'+ sexo +'"'
	sql = sql + ' ORDER BY n.id, nombre '
		
	a = connection.cursor()
	a.execute(sql)
	alumnos = dictfetchall(a)
	
	if alumnos != []:
		if funcion == 'Comprobar':
			return JsonResponse({'estado': 1})
		elif funcion == 'Imprimir':
			num = 0
			for alumno in alumnos:
				num = num + 1
				if num < 10:
					alumno['num'] = '0' + str(num)
				else:
					alumno['num'] = str(num)
				if alumno['estado'] == 1:
					alumno['estado'] = 'Activo'
				else:
					alumno['estado'] = 'Inactivo'
				alumno['edad'] = calcular_edad(alumno['fecha'])
			pagesize = 'Letter'
			html = render_to_string('pdf_catedra.html', locals(), context_instance=RequestContext(request))
			return generar_pdf(html)
	else:
		return JsonResponse({'estado': 3})

# @login_required
# def mostrar_clase(request, clase, cedula, estado, sexo, funcion):
# 	sql = 'SELECT CONCAT(a.nombres ," ", a.apellidos) AS nombre, a.cedula, a.fecha_nacimiento AS fecha, a.sexo, a.activo AS estado, n.nombre AS nivel FROM alumnos_alumno a, alumnos_clase_catedra acc, clases_clase cl, clases_nivel n, clases_catedra c, horarios_horario h, clases_seccion s WHERE a.id = acc.alumno_id AND acc.horario_id = h.id AND h.clase_id = cl.id AND cl.nivel_id = n.id AND cl.catedra_id = c.id AND cl.seccion_id = s.id AND cl.id = "' + clase + '"'
# 	# if clase != 'todos':
# 		# sql = sql + ' AND cl.id = ' + '"'+ clase +'"'
# 	clase = Clase.objects.get(id=clase)
# 	# if nivel != 'todos':
# 		# sql = sql + ' AND n.id = ' + '"'+ nivel +'"'
# 		# nivel = Nivel_I.objects.get(id=nivel)
# 	if cedula != 'todos':
# 		sql = sql + ' AND a.menor = ' + '"'+ cedula +'"'
# 	if estado != 'todos':
# 		sql = sql + ' AND a.activo = ' + '"'+ estado +'"'
# 	if sexo != 'todos':
# 		sql = sql + ' AND a.sexo = ' + '"'+ sexo +'"'
# 	sql = sql + ' ORDER BY n.id, s.id, nombre '
		
# 	a = connection.cursor()
# 	a.execute(sql)
# 	alumnos = dictfetchall(a)
	
# 	if alumnos != []:
# 		if funcion == 'Comprobar':
# 			return JsonResponse({'estado': 1})
# 		elif funcion == 'Imprimir':
# 			num = 0
# 			for alumno in alumnos:
# 				num = num + 1
# 				if num < 10:
# 					alumno['num'] = '0' + str(num)
# 				else:
# 					alumno['num'] = str(num)
# 				if alumno['estado'] == 1:
# 					alumno['estado'] = 'Activo'
# 				else:
# 					alumno['estado'] = 'Inactivo'
# 				alumno['edad'] = calcular_edad(alumno['fecha'])
# 			modulo = 'reportes'
# 			pagesize = 'Letter'
# 			html = render_to_string('pdf_clase.html', locals(), context_instance=RequestContext(request))
# 			return generar_pdf(html)
# 	else:
# 		return JsonResponse({'estado': 3})

##########################################################################################################
def calcular_edad(fecha, hoy=None):
	hoy = hoy or datetime.date.today()
	edad = ((hoy.year - fecha.year - 1) + (1 if (hoy.month, hoy.day) >= (fecha.month, fecha.day) else 0))
	return edad
	
def dictfetchall(cursor):
	desc = cursor.description
	return [
		dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
	]

def cargar_combo(request):
	if request.is_ajax():
		accion = Bitacora.objects.filter(modulo=request.POST['modulo']).values('accion').distinct()
		
		acciones = list(accion)
		# print (acciones)
		return JsonResponse({'acciones': acciones})
	else:
		raise Http404
		
##################################-Para PDF-##################################
def generar_pdf(html):
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))
##################################-Para PDF-##################################