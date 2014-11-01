# -- coding: utf-8 --
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from profesores.models import Profesor
from .models import Catedra, Seccion, Nivel, Clase
from alumnos.models import Clase_Catedra
from horarios.models import Horario
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
	template = 'index_clases.html'
	return render(request, template)

@login_required
def buscar_clase(request, id):
	if request.is_ajax():
		clase = Clase.objects.get(id=id)
		return JsonResponse({'catedra': clase.catedra_id, 'profesor': clase.profesor_id, 'nivel': clase.nivel_id, 'seccion': clase.seccion_id, 'cupo': clase.cupo_max })
	else:
		raise Http404

@login_required
def buscar_visualizar_clase(request, id):
	if request.is_ajax():
		template = 'visualizar_clase.html'
		alumnos = Clase_Catedra.objects.filter(clase_id=id, alumno_id__activo=True)
		for alumno in alumnos:
			alumno.edad = calcular_edad(alumno.alumno.fecha_nacimiento)
		clase = Clase.objects.get(id=id)
		try:
			horarios = Horario.objects.filter(clase_id=id)
		except Exception:
			return render(request, template, locals())
		max = Clase.objects.values('cupo_max').filter(id=id)
		used = Clase_Catedra.objects.filter(clase_id=id, alumno_id__activo=True).count()
		disponible = int(max[0]['cupo_max']) - int(used)
		return render(request, template, locals())

	else:
		raise Http404

@login_required
def guardar_clase(request):
	if request.is_ajax() and request.POST:
		cambio = bool()
		clase = Clase.objects.filter(id=request.POST['id'])
		for dato in clase:
			if str(dato.profesor.id) != request.POST['profesor'] or str(dato.nivel.id) != request.POST['nivel'] or str(dato.seccion.id) != request.POST['seccion'] or str(dato.cupo_max) != request.POST['cupo']:
				if str(dato.nivel.id) == request.POST['nivel'] and str(dato.seccion.id) == request.POST['seccion'] and str(dato.cupo_max) != request.POST['cupo'] or str(dato.profesor.id) != request.POST['profesor']:
					antes = 'Clase: "'+ str(dato.catedra) +' '+ str(dato.nivel) +' '+ str(dato.seccion) +'"'+', Profesor: '+'"'+ str(dato.profesor) +'"'+', Cupo: '+'"'+ str(dato.cupo_max) +'"'
					try:
						clase.update(profesor=request.POST['profesor'], cupo_max=request.POST['cupo'])
					except Exception:
						return JsonResponse({'estado': 0})
					clase = Clase.objects.filter(id=request.POST['id'])
					for dato in clase:
						ahora = 'Clase: "'+ str(dato.catedra) +' '+ str(dato.nivel) +' '+ str(dato.seccion) +'"'+', Profesor: '+'"'+ str(dato.profesor) +'"'+', Cupo: '+'"'+ str(dato.cupo_max) +'"'
					set_bitacora(request, 'Clases', 'Editar', 'Antes['+ antes +']'+' - Ahora['+ ahora +']')
					return JsonResponse({'estado': 1})
				else:
					if Clase.objects.filter(catedra_id=request.POST['catedra'], nivel_id=request.POST['nivel'], seccion_id=request.POST['seccion']):
						return JsonResponse({'estado': 2})
					else:
						antes = 'Catedra: '+'"'+ str(dato.catedra) +'"'+', Profesor: '+'"'+ str(dato.profesor) +'"'+', Nivel: '+'"'+ str(dato.nivel) +'"'+', Seccion: '+'"'+ str(dato.seccion) +'"'+', Cupo: '+'"'+ str(dato.cupo_max) +'"'
			else:
				return JsonResponse({'estado': 3})
			
			if 'antes' in locals():
				try:
					clase.update(profesor=request.POST['profesor'], nivel=request.POST['nivel'], seccion=request.POST['seccion'], cupo_max=request.POST['cupo'])
				except Exception:
					return JsonResponse({'estado': 0})
				clase = Clase.objects.filter(id=request.POST['id'])
				for dato in clase:
					ahora = 'Catedra: '+'"'+ str(dato.catedra) +'"'+', Profesor: '+'"'+ str(dato.profesor) +'"'+', Nivel: '+'"'+ str(dato.nivel) +'"'+', Seccion: '+'"'+ str(dato.seccion) +'"'+', Cupo: '+'"'+ str(dato.cupo_max) +'"'
				set_bitacora(request, 'Clases', 'Editar', 'Antes['+ antes +']'+' - Ahora['+ ahora +']')
				return JsonResponse({'estado': 1})
	else:
		raise Http404

@login_required
def crear(request):
	if request.is_ajax():
		catedras = Catedra.objects.order_by('id').all()
		profesores = Profesor.objects.order_by('nombres').all()
		niveles = Nivel.objects.order_by('id').all()
		secciones = Seccion.objects.order_by('id').all()
		template = 'crear_clase.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def crear_clase(request):
	if request.is_ajax() and request.POST:
		try:
			if Clase.objects.filter(catedra_id=request.POST['catedra'], nivel_id=request.POST['nivel'], seccion_id=request.POST['seccion']):
				return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist # Laza la exepcion de que no existe el obejeto
		except ObjectDoesNotExist:
			try:
				clase = Clase(catedra_id=request.POST['catedra'], profesor_id=request.POST['profesor'], nivel_id=request.POST['nivel'], seccion_id=request.POST['seccion'], cupo_max=request.POST['cupos'])
				clase.save()
				clase = Clase.objects.filter(catedra_id=request.POST['catedra'], nivel_id=request.POST['nivel'], seccion_id=request.POST['seccion'])
				for self in clase:
					set_bitacora(request, 'Clases', 'Crear', 'Catedra: "'+ str(self.catedra) +'"'+', Profesor: "'+ str(self.profesor) +'"'+', Nivel: "'+ str(self.nivel) +'"'+', Seccion: "'+ str(self.seccion) +'"'+', Cupo: "'+ str(self.cupo_max) +'"')
				return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			except Exception:
				return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def editar(request):
	if request.is_ajax():
		clases = Clase.objects.order_by('catedra', 'nivel', 'seccion').all()
		catedras = Catedra.objects.order_by('id').all()
		profesores = Profesor.objects.order_by('nombres').all()
		niveles = Nivel.objects.order_by('id').all()
		secciones = Seccion.objects.order_by('id').all()
		template = 'editar_clase.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def visualizar(request):
	if request.is_ajax():
		clases = Clase.objects.order_by('catedra', 'nivel', 'seccion').all()
		template = 'index_visualizar_clase.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def visualizar_pdf(request, id):
	try:
		clase = Clase.objects.get(id=id)
		horario = Horario.objects.filter(clase_id=id)
		alumnos = Clase_Catedra.objects.filter(clase_id=id, alumno_id__activo=True)
		num = 0
		for alumno in alumnos:
			num = num + 1
			if num < 10:
				alumno.num = '0' + str(num)
			else:
				alumno.num = str(num)
			alumno.edad = calcular_edad(alumno.alumno.fecha_nacimiento)
		pagesize = 'Letter'
		html = render_to_string('pdf_clase.html', locals(), context_instance=RequestContext(request))
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