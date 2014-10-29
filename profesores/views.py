# -- coding: utf-8 --
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from .models import Profesor, Cargo, Designacion
from actividades.models import Tipo_Actividad, Actividad
from alumnos.models import Clase_Individual
from horarios.models import Horario
from sistema.bitacora import set_bitacora

@login_required
def index(request):
	template = 'index_profesor.html'
	return render(request, template)

@login_required
def buscar_profesor(request, id):
	if request.is_ajax():
		profesor = Profesor.objects.get(id=id)
		return JsonResponse({'nombres': profesor.nombres, 'apellidos': profesor.apellidos, 'cedula': profesor.cedula, 'activo': profesor.activo })
	else:
		raise Http404

@login_required
def buscar_editar_profesor(request, id):
	if request.is_ajax():
		profesor = Profesor.objects.get(id=id)
		actividades = Actividad.objects.all().order_by('nombre')
		actividades_profesor = Designacion.objects.filter(profesor_id=id)
		cargos = Cargo.objects.order_by('id').all()
		template = 'editar_profesor.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def buscar_visualizar_profesor(request, id):
	if request.is_ajax():
		profesor = Profesor.objects.get(id=id)
		instrumentos = Clase_Individual.objects.filter(profesor_id=id)
		actividades = Designacion.objects.filter(profesor_id=id)
		clases = Horario.objects.filter(clase__profesor_id=id)
		template = 'visualizar_profesor.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def designar(request):
	if request.is_ajax():
		profesores = Profesor.objects.order_by('nombres').all()
		actividades = Actividad.objects.order_by('nombre').all()
		cargos = Cargo.objects.order_by('id').all()
		template = 'designar_profesor.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def designar_profesor(request):
	if request.is_ajax() and request.POST:
		try:
			if Designacion.objects.filter(actividad_id=request.POST['actividad'], profesor_id=request.POST['profesor']):
				return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
			if Designacion.objects.filter(actividad_id=request.POST['actividad'], cargo_id=request.POST['cargo']):
				return JsonResponse({'estado': 22}) # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist # Laza la exepcion de que no existe el obejeto
		except ObjectDoesNotExist:
			try:
				designacion = Designacion(actividad_id=request.POST['actividad'], profesor_id=request.POST['profesor'], cargo_id=request.POST['cargo'])
				designacion.save()
				datos = Designacion.objects.filter(actividad_id=request.POST['actividad'], profesor_id=request.POST['profesor'])
				for self in datos:
					profesor = str(self.profesor)
					actividad = str(self.actividad)
					cargo = str(self.cargo)
				set_bitacora(request, 'Profesores', 'Designar', 'Profesor: '+ profesor +' | Actividad: "'+ actividad +'"'+', Cargo: "'+ cargo +'"')						
				return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			except Exception:
				return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def editar(request):
	if request.is_ajax():
		profesores = Profesor.objects.all().order_by('nombres')
		template = 'index_editar_profesor.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def guardar_actividad(request):
	if request.is_ajax() and request.POST:
		data = json.loads(request.body)
		cambio = bool()
		ocupado = list()
		for item in data['items']:
			for dato in item:
				actividad = Designacion.objects.filter(id=dato['id'], profesor_id=dato['profesor'])
				for self in actividad:
					if str(self.actividad.id) != str(dato['actividad']) or str(self.cargo.id) != str(dato['cargo']):
						designacion = Designacion.objects.filter(actividad_id=dato['actividad'], cargo_id=dato['cargo'])
						if designacion:
							ocupado.append({'actividad': str(designacion[0].actividad), 'cargo': str(designacion[0].cargo)})
						else:
							antes = 'Actividad: '+'"'+ str(self.actividad) +'"'+', Cargo: '+'"'+ str(self.cargo) +'"'
				if 'antes' in locals():
					actividad.update(actividad=dato['actividad'], cargo=dato['cargo'])
					cambio = True
					actividad = Designacion.objects.filter(id=dato['id'], profesor_id=dato['profesor'])			
					for self in actividad:
						profesor = str(self.profesor)
						ahora = 'Actividad: '+'"'+ str(self.actividad) +'"'+', Cargo: '+'"'+ str(self.cargo) +'"'
					set_bitacora(request, 'Profesores', 'Editar', 'Profesor: '+ profesor +' | Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')					
					del antes
		if cambio:
			if ocupado:
				return JsonResponse({'estado': 1, 'ocupado': ocupado}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		else:
			if ocupado:
				return JsonResponse({'estado': 3, 'ocupado': ocupado}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			return JsonResponse({'estado': 3}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def guardar_datos(request):
	if request.is_ajax() and request.POST:
		cambio = bool()
		profesor = Profesor.objects.filter(id=request.POST['id'])
		for dato in profesor:
			if dato.nombres != request.POST['nombres'].title() or dato.apellidos != request.POST['apellidos'].title() or str(dato.cedula) != str(request.POST['cedula']) or dato.activo != bool(int(request.POST['activo'])):
				if dato.activo == True:
					estado = 'Activo'
				else:
					estado = 'Inactivo'
				antes = 'Nombres: '+'"'+ dato.nombres +'"'+', '+ unicode('Apellidos: ','utf-8') +'"'+ dato.apellidos +'"'+', '+ unicode('Cédula:','utf-8') +'"'+ str(dato.cedula) +'"'+', Estado: '+'"'+ estado +'"'
		if 'antes' in locals():
			try:
				profesor.update(cedula=request.POST['cedula'], nombres=request.POST['nombres'].title(), apellidos=request.POST['apellidos'].title(), activo=bool(int(request.POST['activo'])))
			except Exception:
				return JsonResponse({'estado': 0})
			cambio = True
			for dato in profesor:
				if dato.activo == True:
					estado = 'Activo'
				else:
					estado = 'Inactivo'
				ahora = 'Nombres: '+'"'+ dato.nombres +'"'+', '+ unicode('Apellidos: ','utf-8') +'"'+ dato.apellidos +'"'+', '+ unicode('Cédula:','utf-8') +'"'+ str(dato.cedula) +'"'+', Estado: '+'"'+ estado +'"'
			set_bitacora(request, 'Profesores', 'Editar', 'Antes['+ antes +']'+' - Ahora['+ ahora +']')
			del antes
		if cambio:
			return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		else:
			return JsonResponse({'estado': 3}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def registrar(request):
	if request.is_ajax():
		template = 'registrar_profesor.html'
		return render(request, template)
	else:
		raise Http404

@login_required
def registrar_profesor(request):
	if request.is_ajax() and request.POST:
		try:
			Profesor.objects.get(cedula=request.POST['cedula'])
			return JsonResponse({'estado': 2}) # Retorna que no es Aceptable	
		except ObjectDoesNotExist:
			try:
				profesor = Profesor(cedula=request.POST['cedula'], nombres=request.POST['nombres'].title(), apellidos=request.POST['apellidos'].title(), activo='1')
				profesor.save()
				set_bitacora(request, 'Profesores', 'Registrar', 'Nombres: "'+ request.POST['nombres'].title() +'"'+', Apellidos: "'+ request.POST['apellidos'].title() +'"'+', Cedula: "'+ request.POST['cedula'] +'"')
				return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			except Exception:
				return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def visualizar(request):
	if request.is_ajax():
		profesores = Profesor.objects.all().order_by('nombres')
		template = 'index_visualizar_profesor.html'
		return render(request, template, locals())
	else:
		raise Http404