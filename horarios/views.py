# -- coding: utf-8 --
import json
import datetime
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context
from django.template.context import RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from .models import Dia, Horario
from clases.models import Clase
from sistema.bitacora import set_bitacora

@login_required
def index(request):
	template = 'index_horarios.html'
	return render(request, template)

@login_required
def crear(request):
	horario = Horario.objects.all()
	ids = list()
	# print (horario)
	for clase in horario:
		ids.append(str(clase.clase_id))

	clases = Clase.objects.exclude(id__in=ids).order_by('catedra', 'nivel', 'seccion')
	dias = Dia.objects.order_by('id').all()
	template = 'crear_horario.html'
	return render(request, template, locals())

@login_required
def crear_horario(request):
	if request.is_ajax() and request.POST:
		try:
			if Horario.objects.filter(clase_id=request.POST['clase']):
				return HttpResponse(json.dumps({'estado': 2}), content_type="application/json; charset=uft8") # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist
		except ObjectDoesNotExist:
			try:
				horario = Horario(clase_id=request.POST['clase'], dia_id=request.POST['dia'], hora_desde=request.POST['desde'], hora_hasta=request.POST['hasta'])
				horario.save()
				horario = Horario.objects.filter(clase_id=request.POST['clase'])
				for self in horario:
					set_bitacora(request, 'Horarios', 'Crear', 'Clase: "'+ str(self.clase) +'"'+', Dia: "'+ str(self.dia) +'"'+', Hora Desde: "'+ str(self.hora_desde) +'"'+', Hora Hasta: "'+ str(self.hora_hasta) +'"')
				return HttpResponse(json.dumps({'estado': 1}), content_type="application/json; charset=uft8") # Retorna que se ha creado un nuevo recurso de forma exitosa
			except Exception:
				return HttpResponse(json.dumps({'estado': 0}), content_type="application/json; charset=uft8") # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def editar(request):
	dias = Dia.objects.all().order_by('id')
	horarios = Horario.objects.all()
	template = 'editar_horario.html'
	return render(request, template, locals())

@login_required
def buscar_horario(request, id):
	if request.is_ajax():
		horario = Horario.objects.get(id=id)
		return HttpResponse(json.dumps({'dia': horario.dia_id, 'desde': horario.hora_desde, 'hasta': horario.hora_hasta}), content_type="application/json; charset=uft8")
	else:
		raise Http404

@login_required
def guardar_horario(request):
	if request.is_ajax() and request.POST:
		horario = Horario.objects.filter(id=request.POST['id'])
		for dato in horario:
			if str(dato.dia.id) != request.POST['dia'] or str(dato.hora_desde) != request.POST['desde'] or str(dato.hora_hasta) != request.POST['hasta']:
				antes = 'Clase: '+'"'+ str(dato.clase) +'"'+', Dia: '+'"'+ str(dato.dia) +'"'+', De: '+'"'+ str(dato.hora_desde) +'"'+' a '+'"'+ str(dato.hora_hasta) +'"'
			else:
				return HttpResponse(json.dumps({'estado': 3}), content_type="application/json; charset=uft8")
		if 'antes' in locals():
			try:
				horario.update(dia=request.POST['dia'], hora_desde=request.POST['desde'], hora_hasta=request.POST['hasta'])
			except Exception:
				return HttpResponse(json.dumps({'estado': 0}), content_type="application/json; charset=uft8")
			horario = Horario.objects.filter(id=request.POST['id'])
			for dato in horario:
				ahora = 'Clase: '+'"'+ str(dato.clase) +'"'+', Dia: '+'"'+ str(dato.dia) +'"'+', De: '+'"'+ str(dato.hora_desde) +'"'+' a '+'"'+ str(dato.hora_hasta) +'"'
			set_bitacora(request, 'Horarios', 'Editar', 'Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')
			return HttpResponse(json.dumps({'estado': 1}), content_type="application/json; charset=uft8")
	else:
		raise Http404

