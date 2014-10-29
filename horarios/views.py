# -- coding: utf-8 --
import json
import datetime, time
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, Http404
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
	for clase in horario:
		ids.append(str(clase.clase_id))

	clases = Clase.objects.exclude(id__in=ids).order_by('catedra', 'nivel', 'seccion')
	dias = Dia.objects.order_by('id').all()
	template = 'crear_horario.html'
	return render(request, template, locals())

@login_required
def crear_horario(request):
	if request.is_ajax() and request.POST:
######################################################################################################################################		
		dato = Clase.objects.get(id=request.POST['clase'])
		clases = Clase.objects.filter(profesor_id=dato.profesor.id)
		for clase in clases:
			horarios = Horario.objects.filter(clase_id=clase.id, dia_id=request.POST['dia'])
			for hora in horarios:
				if choqueHorario(request.POST['desde'], request.POST['hasta'], hora.inicio, hora.final):
					choque = True
		if 'choque' in locals():
			print 'Conflicto'
			return JsonResponse({'choque': 'true'}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		else:
			print 'Horario Aceptable'
######################################################################################################################################		
			try:
				if Horario.objects.filter(clase_id=request.POST['clase']):
					return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
				else:
					raise ObjectDoesNotExist
			except ObjectDoesNotExist:
				try:
					horario = Horario(clase_id=request.POST['clase'], dia_id=request.POST['dia'], inicio=request.POST['desde'], final=request.POST['hasta'])
					horario.save()
					horario = Horario.objects.filter(clase_id=request.POST['clase'])
					for self in horario:
						set_bitacora(request, 'Horarios', 'Crear', 'Clase: "'+ str(self.clase) +'"'+', Dia: "'+ str(self.dia) +'"'+', Hora Desde: "'+ str(self.inicio) +'"'+', Hora Hasta: "'+ str(self.final) +'"')
					return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
				except Exception:
					return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def editar(request):
	dias = Dia.objects.all().order_by('id')
	horarios = Horario.objects.all().order_by('clase__catedra', 'clase__nivel', 'clase__seccion')
	template = 'editar_horario.html'
	return render(request, template, locals())

@login_required
def buscar_horario(request, id):
	if request.is_ajax():
		horario = Horario.objects.get(id=id)
		return JsonResponse({'dia': horario.dia_id, 'desde': horario.inicio, 'hasta': horario.final})
	else:
		raise Http404

@login_required
def guardar_horario(request):
	if request.is_ajax() and request.POST:
		horario = Horario.objects.filter(id=request.POST['id'])
		for dato in horario:
			if str(dato.dia.id) != request.POST['dia'] or str(dato.inicio) != request.POST['desde'] or str(dato.final) != request.POST['hasta']:
######################################################################################################################################		
				dato_p = Clase.objects.get(id=dato.clase.id)
				clases = Clase.objects.filter(profesor_id=dato_p.profesor.id).exclude(id=dato.clase.id)
				for clase in clases:
					horarios = Horario.objects.filter(clase_id=clase.id, dia_id=request.POST['dia'])
					for hora in horarios:
						if choqueHorario(request.POST['desde'], request.POST['hasta'], hora.inicio, hora.final):
							choque = True
				if 'choque' in locals():
					print 'Conflicto'
					return JsonResponse({'choque': 'true'}) # Retorna que se ha creado un nuevo recurso de forma exitosa
				else:
					print 'Horario Aceptable'
######################################################################################################################################		
					antes = 'Clase: '+'"'+ str(dato.clase) +'"'+', Dia: '+'"'+ str(dato.dia) +'"'+', De: '+'"'+ str(dato.inicio) +'"'+' a '+'"'+ str(dato.final) +'"'
			else:
				return JsonResponse({'estado': 3})
		if 'antes' in locals():
			try:
				horario.update(dia=request.POST['dia'], inicio=request.POST['desde'], final=request.POST['hasta'])
			except Exception:
				return JsonResponse({'estado': 0})
			horario = Horario.objects.filter(id=request.POST['id'])
			for dato in horario:
				ahora = 'Clase: '+'"'+ str(dato.clase) +'"'+', Dia: '+'"'+ str(dato.dia) +'"'+', De: '+'"'+ str(dato.inicio) +'"'+' a '+'"'+ str(dato.final) +'"'
			set_bitacora(request, 'Horarios', 'Editar', 'Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')
			return JsonResponse({'estado': 1})
	else:
		raise Http404

def choqueHorario(nuevoInicio, nuevoFinal, inicio, final):
	nuevoInicio = convertirHora(nuevoInicio)
	nuevoFinal = convertirHora(nuevoFinal)
	inicio = convertirHora(inicio)
	final = convertirHora(final)
	if nuevoInicio >= final and nuevoFinal >= inicio or nuevoInicio <= final and nuevoFinal <= inicio:
		return False
	else:
		return True

def convertirHora(hora):
	hora = time.strptime(hora, '%I:%M %p')
	if hora.tm_hour < 10:
		horas = '0'+str(hora.tm_hour)
	else:
		horas = str(hora.tm_hour)
	if hora.tm_min < 10:
		minutos = '0'+str(hora.tm_min)
	else:
		minutos = str(hora.tm_min)
	return horas+':'+minutos