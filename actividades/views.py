# -- coding: utf-8 --
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from .models import Tipo_Actividad, Nivel_Actividad, Actividad
from alumnos.models import Alumno_Actividad
from profesores.models import Designacion
from sistema.bitacora import set_bitacora

##################################-Para PDF-##################################
import cgi
import ho.pisa as pisa
import cStringIO as StringIO
from django.db import connection
from django.template import RequestContext
from django.template.loader import render_to_string
##################################-Para PDF-##################################

@login_required
def index(request):
	template = 'index_actividades.html'
	return render(request, template)

@login_required
def buscar_actividad(request, id):
	if request.is_ajax():
		actividad = Actividad.objects.get(id=id)
		return HttpResponse(json.dumps({'nombre': actividad.nombre, 'tipo': actividad.tipo_id, 'nivel': actividad.nivel_id}), content_type="application/json; charset=uft8")
	else:
		raise Http404

@login_required
def buscar_visualizar_actividad(request, id):
	if request.is_ajax():
		template = 'visualizar_actividad.html'
		alumnos = Alumno_Actividad.objects.filter(actividad_id=id, alumno_id__activo=True)
		actividad = Actividad.objects.get(id=id)
		for alumno in alumnos:
			alumno.edad = calcular_edad(alumno.alumno.fecha_nacimiento)
		try:
			director = Designacion.objects.get(actividad_id=id, cargo__nombre='Director')
		except Exception:
			pass
		try:
			asistente = Designacion.objects.get(actividad_id=id, cargo__nombre='Asistente')
		except Exception:
			pass
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def guardar_actividad(request):
	if request.is_ajax() and request.POST:
		actividad = Actividad.objects.filter(id=request.POST['id'])	
		for dato in actividad:
			if str(dato.nombre) != request.POST['nombre'].title() or str(dato.nivel.id) != request.POST['nivel']:
				antes = 'Nombre: '+'"'+ str(dato.nombre) +'"'+', Nivel: '+'"'+ str(dato.nivel) +'"'
			else:
				return HttpResponse(json.dumps({'estado': 3}), content_type="application/json; charset=uft8")
		if 'antes' in locals():
			try:
				actividad.update(nombre=request.POST['nombre'].title(), nivel=request.POST['nivel'])
			except Exception:
				return HttpResponse(json.dumps({'estado': 0}), content_type="application/json; charset=uft8")
			actividad = Actividad.objects.filter(id=request.POST['id'])	
			for dato in actividad:
				ahora = 'Nombre: '+'"'+ str(dato.nombre) +'"'+', Nivel: '+'"'+ str(dato.nivel) +'"'
			set_bitacora(request, 'Actividades', 'Editar', 'Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')
			return HttpResponse(json.dumps({'estado': 1}), content_type="application/json; charset=uft8")
	else:
		raise Http404

@login_required
def crear(request):
	if request.is_ajax():
		niveles = Nivel_Actividad.objects.order_by('id').all()
		tipos = Tipo_Actividad.objects.order_by('id').all()
		template = 'crear_actividad.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def crear_actividad(request):
	if request.is_ajax() and request.POST:
		try:
			if Actividad.objects.filter(nombre=request.POST['nombre'].title(), tipo_id=request.POST['tipo'], nivel_id=request.POST['nivel']):
				return HttpResponse(json.dumps({'estado': 2}), content_type="application/json; charset=uft8") # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist
		except ObjectDoesNotExist:
			try:
				actividad = Actividad(nombre=request.POST['nombre'].title(), tipo_id=request.POST['tipo'], nivel_id=request.POST['nivel'])
				actividad.save()
			except Exception, e:
				return HttpResponse(json.dumps({'estado': 0}), content_type="application/json; charset=uft8") # Retorna que se ha creado un nuevo recurso de forma exitosa
			actividad = Actividad.objects.filter(nombre=request.POST['nombre'].title(), tipo_id=request.POST['tipo'], nivel_id=request.POST['nivel'])
			for dato in actividad:
				set_bitacora(request, 'Actividades', 'Crear', 'Nombre: "'+ request.POST['nombre'].title() +'"'+', Tipo: "'+ unicode(str(dato.tipo), 'utf-8') +'"'+', Nivel: "'+ unicode(str(dato.nivel), 'utf-8') +'"')
			return HttpResponse(json.dumps({'estado': 1}), content_type="application/json; charset=uft8") # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def editar(request):
	if request.is_ajax():
		actividades = Actividad.objects.order_by('tipo').all()
		niveles = Nivel_Actividad.objects.order_by('id').all()
		tipos = Tipo_Actividad.objects.order_by('id').all()
		template = 'editar_actividad.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def visualizar(request):
	actividades = Actividad.objects.order_by('tipo').all()
	template = 'index_visualizar_actividad.html'
	return render(request, template, locals())

@login_required
def visualizar_pdf(request, id):
	try:
		actividad = Actividad.objects.get(id=id)
		alumnos = Alumno_Actividad.objects.filter(actividad_id=id)
		num = 0
		for alumno in alumnos:
			num = num + 1
			if num < 10:
				alumno.num = '0' + str(num)
			else:
				alumno.num = str(num)
			alumno.edad = calcular_edad(alumno.alumno.fecha_nacimiento)
		try:
			director = Designacion.objects.get(actividad_id=actividad, cargo__nombre='Director')
		except Exception:
			pass
		try:
			asistente = Designacion.objects.get(actividad_id=actividad, cargo__nombre='Asistente')
		except Exception:
			pass
		pagesize = 'Letter'
		html = render_to_string('pdf_actividad.html', locals(), context_instance=RequestContext(request))
		return generar_pdf(html)
	except Exception:
		raise Http404

def calcular_edad(fecha, hoy=None):
	hoy = hoy or datetime.date.today()
	edad = ((hoy.year - fecha.year - 1) + (1 if (hoy.month, hoy.day) >= (fecha.month, fecha.day) else 0))
	return edad

##################################-Para PDF-##################################
def generar_pdf(html):
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))
##################################-Para PDF-##################################