# -- coding: utf-8 --
import json
import datetime, time
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
	for clase in horario:
		ids.append(str(clase.clase_id))

	clases = Clase.objects.exclude(id__in=ids).order_by('catedra', 'nivel', 'seccion')
	dias = Dia.objects.order_by('id').all()
	template = 'crear_horario.html'
	return render(request, template, locals())

@login_required
def crear_horario(request):
	if request.is_ajax() and request.POST:
		dato = Clase.objects.get(id=request.POST['clase'])
		clases = Clase.objects.filter(profesor_id=dato.profesor.id)
		print 'Profesor:',dato.profesor.id
		i = int()
		for clase in clases:
			i = i+1
			print 'Vez:',i
			horarios = Horario.objects.filter(clase_id=clase.id, dia_id=request.POST['dia'])
			for hora in horarios:
				print 'Horas Inicio:',request.POST['desde'], request.POST['hasta'],' - ', hora.inicio, hora.final
				conflictoHoraInicio(request.POST['desde'], request.POST['hasta'], hora.inicio, hora.final)

		return HttpResponse(status=200)
		# if conflictoHora(request.POST['desde'], '2:00 pm') or conflictoHora('2:45 pm', equest.POST['hasta']):
			# pass
		# try:
		# 	if Horario.objects.filter(clase_id=request.POST['clase']):
		# 		return HttpResponse(json.dumps({'estado': 2}), content_type="application/json; charset=uft8") # Retorna que no es Aceptable
		# 	else:
		# 		raise ObjectDoesNotExist
		# except ObjectDoesNotExist:
		# 	try:
		# 		horario = Horario(clase_id=request.POST['clase'], dia_id=request.POST['dia'], inicio=request.POST['desde'], final=request.POST['hasta'])
		# 		horario.save()
		# 		horario = Horario.objects.filter(clase_id=request.POST['clase'])
		# 		for self in horario:
		# 			set_bitacora(request, 'Horarios', 'Crear', 'Clase: "'+ str(self.clase) +'"'+', Dia: "'+ str(self.dia) +'"'+', Hora Desde: "'+ str(self.inicio) +'"'+', Hora Hasta: "'+ str(self.final) +'"')
		# 		return HttpResponse(json.dumps({'estado': 1}), content_type="application/json; charset=uft8") # Retorna que se ha creado un nuevo recurso de forma exitosa
		# 	except Exception:
		# 		return HttpResponse(json.dumps({'estado': 0}), content_type="application/json; charset=uft8") # Retorna que se ha creado un nuevo recurso de forma exitosa
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
		return HttpResponse(json.dumps({'dia': horario.dia_id, 'desde': horario.inicio, 'hasta': horario.final}), content_type="application/json; charset=uft8")
	else:
		raise Http404

@login_required
def guardar_horario(request):
	if request.is_ajax() and request.POST:
		horario = Horario.objects.filter(id=request.POST['id'])
		for dato in horario:
			if str(dato.dia.id) != request.POST['dia'] or str(dato.inicio) != request.POST['desde'] or str(dato.final) != request.POST['hasta']:
				antes = 'Clase: '+'"'+ str(dato.clase) +'"'+', Dia: '+'"'+ str(dato.dia) +'"'+', De: '+'"'+ str(dato.inicio) +'"'+' a '+'"'+ str(dato.final) +'"'
			else:
				return HttpResponse(json.dumps({'estado': 3}), content_type="application/json; charset=uft8")
		if 'antes' in locals():
			try:
				horario.update(dia=request.POST['dia'], inicio=request.POST['desde'], final=request.POST['hasta'])
			except Exception:
				return HttpResponse(json.dumps({'estado': 0}), content_type="application/json; charset=uft8")
			horario = Horario.objects.filter(id=request.POST['id'])
			for dato in horario:
				ahora = 'Clase: '+'"'+ str(dato.clase) +'"'+', Dia: '+'"'+ str(dato.dia) +'"'+', De: '+'"'+ str(dato.inicio) +'"'+' a '+'"'+ str(dato.final) +'"'
			set_bitacora(request, 'Horarios', 'Editar', 'Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')
			return HttpResponse(json.dumps({'estado': 1}), content_type="application/json; charset=uft8")
	else:
		raise Http404

def conflictoHoraInicio(nuevoInicio, nuevoFinal, inicio, final):
	if inicio < final:
		print 'Conflicto'
	else:
		print 'Todo BN'
