# -- coding: utf-8 --
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context
from django.template.context import RequestContext
from django.template.loader import get_template
from instrumentos.models import Tipo_Instrumento, Instrumento
from actividades.models import Tipo_Actividad, Nivel_Actividad
from alumnos.models import Nivel_I
from clases.models import Catedra, Seccion, Nivel
from horarios.models import Dia
from profesores.models import Cargo


@login_required
def index(request):
	tipo_instrumento = Tipo_Instrumento.objects.count()
	instrumento = Instrumento.objects.count()
	tipo_actividad = Tipo_Actividad.objects.count()
	nivel_actividad = Nivel_Actividad.objects.count()
	nivel_i = Nivel_I.objects.count()
	catedra = Catedra.objects.count()
	seccion = Seccion.objects.count()
	nivel = Nivel.objects.count()
	dia = Dia.objects.count()
	cargo = Cargo.objects.count()
	user = User.objects.count()
	if int(user) > 0 and int(tipo_instrumento) == 0 and int(instrumento) == 0 and int(tipo_actividad) == 0 and int(nivel_actividad) == 0 and int(nivel_i) == 0 and int(catedra) == 0 and int(seccion) == 0 and int(nivel) == 0 and int(dia) == 0 and int(cargo) == 0:
		print 'Cargar datos...'
		import cargar
	else:
		print '¡No hay carga de datos!'
	
	template = 'index.html'
	return render(request, template)