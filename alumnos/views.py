# -- coding: utf-8 --
import json
import datetime, time
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.context import RequestContext
from .models import Alumno, Prenda, Alumno_Prenda, Alumno_Actividad, Nivel_I, Clase_Individual, Clase_Catedra
from actividades.models import Tipo_Actividad, Actividad
from clases.models import Clase
from horarios.models import Horario
from instrumentos.models import Instrumento
from profesores.models import Profesor
from sistema.bitacora import set_bitacora

@login_required
def index(request):
	template = 'index_alumno.html'
	return render(request, template)

@login_required
def actividad(request, id):
	if request.is_ajax():
		alumno = Alumno_Actividad.objects.filter(alumno_id=id)
		ids = list()
		for actividad in alumno:
			ids.append(str(actividad.actividad_id))
		actividades = Actividad.objects.exclude(id__in=ids).order_by('tipo')
		tipos = Tipo_Actividad.objects.all()
		individuales = Clase_Individual.objects.filter(alumno_id=id).order_by('id')
		instrumentos = Instrumento.objects.filter(instrumento__nombre='Voz').order_by('id')
		template = 'asignar_actividad.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def asignar(request):
	if request.is_ajax():
		template = 'asignar_alumno.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def asignar_actividad(request):
	if request.is_ajax() and request.POST:
		try:
			if Alumno_Actividad.objects.filter(alumno_id=request.POST['alumno'], actividad_id=request.POST['actividad']):
				return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist # Laza la exepcion de que no existe el obejeto
		except ObjectDoesNotExist:
			try:
				actividad = Alumno_Actividad(alumno_id=request.POST['alumno'], actividad_id=request.POST['actividad'], instrumento_id=request.POST['instrumento'], clasificacion=request.POST['clasificacion'])
				actividad.save()
				datos = Alumno_Actividad.objects.filter(alumno_id=request.POST['alumno'], actividad_id=request.POST['actividad'])
				for self in datos:
					set_bitacora(request, 'Alumnos', 'Asignar', 'Alumno: '+ str(self.alumno) +' | Actividad: "'+ str(self.actividad) +'"'+' Instrumento: "'+ str(self.instrumento) +'"'+' Clasificación: "'+ str(self.clasificacion) +'"')
				return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			except Exception:
				return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def asignar_catedra(request):
	if request.is_ajax() and request.POST:
		try:
			if Clase_Catedra.objects.filter(alumno_id=request.POST['alumno'], clase_id=request.POST['clase']):
				return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
			elif Clase_Catedra.objects.filter(alumno_id=request.POST['alumno'], clase_id__catedra_id=request.POST['catedra']):
				return JsonResponse({'estado': 2.1}) # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist # Laza la exepcion de que no existe el obejeto
		except ObjectDoesNotExist:
######################################################################################################################################		
			horarios = Horario.objects.filter(clase_id=request.POST['clase'])
			for horario in horarios:
				datos_clases = Clase_Catedra.objects.filter(alumno_id=request.POST['alumno'])
				for dato_clase in datos_clases:
					datos_horarios = Horario.objects.filter(clase_id=dato_clase.clase.id, dia_id=horario.dia.id)
					for dato_horario in datos_horarios:
						if choqueHorario(horario.inicio, horario.final, dato_horario.inicio, dato_horario.final):
							choque = True
							clase = str(dato_clase.clase)
			if 'choque' in locals():
				print 'Conflicto'
				return JsonResponse({'choque': 'true', 'clase': clase}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			else:
				print 'Horario Aceptable'
######################################################################################################################################		
				clase = Clase.objects.get(id=request.POST['clase'])
				# max = Clase.objects.values('cupo_max').filter(id=request.POST['clase'])
				max = int(clase.cupo_max)
				used = Clase_Catedra.objects.filter(clase_id=request.POST['clase']).count()
				disponible = max - int(used)
				if disponible > 0:
					try:
						clase = Clase_Catedra(alumno_id=request.POST['alumno'], clase_id=request.POST['clase'])
						clase.save()
						datos = Clase_Catedra.objects.filter(alumno_id=request.POST['alumno'], clase_id=request.POST['clase'])
						for self in datos:
							set_bitacora(request, 'Alumnos', 'Asignar', 'Alumno: '+ str(self.alumno) +' | Cátedra: "'+ str(self.clase) +'"')
						return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
					except Exception:
						return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
				else:
					return JsonResponse({'estado': 3}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def asignar_clase_individual(request):
	if request.is_ajax() and request.POST:
		try:
			if Clase_Individual.objects.filter(alumno_id=request.POST['alumno'], instrumento_id=request.POST['instrumento']):
				return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist # Laza la exepcion de que no existe el obejeto
		except ObjectDoesNotExist:
			try:
				individual = Clase_Individual(alumno_id=request.POST['alumno'], profesor_id=request.POST['profesor'], instrumento_id=request.POST['instrumento'], nivel_id=request.POST['nivel'])
				individual.save()
				datos = Clase_Individual.objects.filter(alumno_id=request.POST['alumno'], instrumento_id=request.POST['instrumento'])
				for self in datos:
					set_bitacora(request, 'Alumnos', 'Asignar', 'Alumno: '+ str(self.alumno) +' | Instrumento: "'+ str(self.instrumento) +'"'+' Profesor: "'+ str(self.profesor) +'"'+' Nivel: "'+ str(self.nivel) +'"')
				return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			except Exception:
				return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def asignar_talla(request):
	if request.is_ajax() and request.POST:
		try:
			if Alumno_Prenda.objects.filter(alumno_id=request.POST['alumno'], prenda_id=request.POST['prenda']):
				prenda = Prenda.objects.get(id=int(request.POST['prenda']))
				return JsonResponse({'estado': 2, 'prenda': str(prenda)}) # Retorna que no es Aceptable
			else:
				raise ObjectDoesNotExist # Laza la exepcion de que no existe el obejeto
		except ObjectDoesNotExist:
			try:
				prenda = Alumno_Prenda(alumno_id=request.POST['alumno'], prenda_id=request.POST['prenda'], talla=request.POST['talla'].upper(), otorgado=bool(int(request.POST['otorgado'])))
				prenda.save()
				datos = Alumno_Prenda.objects.filter(alumno_id=request.POST['alumno'], prenda_id=request.POST['prenda'])
				for self in datos:
					prenda = str(self.prenda)
					set_bitacora(request, 'Alumnos', 'Asignar', 'Alumno: '+ str(self.alumno) +' | Prenda: "'+ str(self.prenda) +'"'+' Talla: "'+ str(self.talla) +'"'+' Otorgado: "'+ str(self.otorgado) +'"')
				return JsonResponse({'estado': 1, 'prenda': prenda}) # Retorna que se ha creado un nuevo recurso de forma exitosa
			except Exception:
				return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def buscar_asignar_alumno(request, id):
	if request.is_ajax():
		alumno = Alumno.objects.get(id=id)
		return JsonResponse({'id': id, 'nombres': alumno.nombres, 'apellidos': alumno.apellidos, 'cedula': alumno.cedula, 'sexo': alumno.sexo, 'fecha': str(alumno.fecha_nacimiento), 'activo': alumno.activo})
	else:
		raise Http404

@login_required
def buscar_editar_alumno(request, id):
	if request.is_ajax():
		alumno = Alumno.objects.get(id=id)
		prendas = Alumno_Prenda.objects.filter(alumno_id=id)
		instrumentos = Instrumento.objects.filter(instrumento__nombre='Clasico').order_by('id')
		individuales = Clase_Individual.objects.filter(alumno_id=id)
		niveles = Nivel_I.objects.order_by('id').all()
		profesores = Profesor.objects.all().order_by('nombres')
		actividades = Actividad.objects.all().order_by('nombre')
		actividades_alumno = Alumno_Actividad.objects.filter(alumno_id=id)
		instrumentos_actividad = Instrumento.objects.filter(instrumento__nombre='Voz').order_by('id')
		clases = Clase.objects.all().order_by('catedra__id', 'nivel__id', 'seccion__id')
		datos_cl = Clase_Catedra.objects.filter(alumno_id=id).order_by('clase_id__catedra_id')
		clases_alumno = list()
		for dato_cl in datos_cl:
			horarios = list()
			datos_h = Horario.objects.filter(clase_id=dato_cl.clase.id)
			for dato_h in datos_h:
				horarios.append({'dia': str(dato_h.dia), 'inicio': str(dato_h.inicio), 'final': str(dato_h.final)})
			clases_alumno.append({'id': dato_cl.id, 'clase_id':dato_cl.clase.id, 'catedra': dato_cl.clase.catedra.id, 'clase': str(dato_cl.clase), 'horarios': horarios})

		# horarios = Horario.objects.all().order_by('clase__catedra', 'clase__nivel__id', 'clase__seccion__id')

		template = 'editar_alumno.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def buscar_visualizar_alumno(request, id):
	if request.is_ajax():
		alumno = Alumno.objects.get(id=id)
		prendas = Alumno_Prenda.objects.filter(alumno_id=id)
		instrumentos = Clase_Individual.objects.filter(alumno_id=id)
		actividades = Alumno_Actividad.objects.filter(alumno_id=id)
		datos_cl = Clase_Catedra.objects.filter(alumno_id=id).order_by('clase_id__catedra_id')
		clases = list()
		for dato_cl in datos_cl:
			horarios = list()
			clase = str(dato_cl.clase)
			datos_h = Horario.objects.filter(clase_id=dato_cl.clase.id)
			for dato_h in datos_h:
				horarios.append({'dia': str(dato_h.dia), 'inicio': str(dato_h.inicio), 'final': str(dato_h.final)})
			clases.append({'clase': clase, 'horarios': horarios})
		template = 'visualizar_alumno.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def buscar_horario(request, id):
	if request.is_ajax():
		datos = Horario.objects.filter(clase_id=id)
		horarios = list()
		for dato in datos:
			horarios.append({'dia': dato.dia.nombre, 'inicio': dato.inicio, 'final': dato.final})
		catedra = datos[0].clase.catedra.id
		clase = datos[0].clase.id
		return JsonResponse({'horarios': horarios, 'catedra': catedra, 'clase': clase})
	else:
		raise Http404

@login_required
def catedra(request, id):
	if request.is_ajax():
		clases = Clase_Catedra.objects.filter(alumno_id=id)
		ids = list()
		for clase in clases:
			ids.append(str(clase.clase.catedra.id))
		# clases = Clase.objects.exclude().order_by('catedra', 'nivel', 'seccion')
		clases = Clase.objects.exclude(catedra_id__in=ids).order_by('catedra', 'nivel', 'seccion')
		template = 'asignar_catedra.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def editar(request):
	if request.is_ajax():
		template = 'index_editar_alumno.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def guardar_actividad(request):
	if request.is_ajax() and request.POST:
		data = json.loads(request.body)
		cambio = bool()
		for item in data['items']:
			for dato in item:
				actividad = Alumno_Actividad.objects.filter(id=dato['id'], alumno_id=dato['alumno'])
				for self in actividad:
					if str(self.actividad.id) != str(dato['actividad']) or str(self.instrumento.id) != str(dato['instrumento']) or str(self.clasificacion) != str(dato['clasificacion']):
						antes = 'Actividad: '+'"'+ str(self.actividad) +'"'+', Instrumento: '+'"'+ str(self.instrumento) +'"'+', Clasificación: '+'"'+ str(self.clasificacion) +'"'
				if 'antes' in locals():
					actividad.update(actividad=dato['actividad'], instrumento=dato['instrumento'], clasificacion=dato['clasificacion'])
					Alumno.objects.filter(id=dato['alumno']).update(fecha_actualizacion=datetime.date.today())
					cambio = True
					actividad = Alumno_Actividad.objects.filter(id=dato['id'], alumno_id=dato['alumno'])			
					for self in actividad:
						alumno = str(self.alumno)
						ahora = 'Actividad: '+'"'+ str(self.actividad) +'"'+', Instrumento: '+'"'+ str(self.instrumento) +'"'+', Clasificación: '+'"'+ str(self.clasificacion) +'"'
					set_bitacora(request, 'Alumnos', 'Editar', 'Alumno: '+ alumno +' | Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')					
					del antes
		if cambio:
			return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		else:
			return JsonResponse({'estado': 3}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def guardar_clase(request):
	if request.is_ajax() and request.POST:
		cambio = bool()
		clase = Clase_Catedra.objects.filter(id=request.POST['id'], alumno_id=request.POST['alumno'])
		for self in clase:
			if str(self.clase.id) != str(request.POST['clase']):
				horarios = Horario.objects.filter(clase_id=request.POST['clase'])
				for horario in horarios:
					datos_clases = Clase_Catedra.objects.filter(alumno_id=request.POST['alumno']).exclude(clase_id=self.clase.id)
					for dato_clase in datos_clases:
						datos_horarios = Horario.objects.filter(clase_id=dato_clase.clase.id, dia_id=horario.dia.id)
						for dato_horario in datos_horarios:
							if choqueHorario(horario.inicio, horario.final, dato_horario.inicio, dato_horario.final):
								choque = True
								choque_clase = str(dato_clase.clase)
				if 'choque' in locals():
					print 'Conflicto'
					return JsonResponse({'choque': 'true', 'clase': choque_clase})
				else:
					print 'Horario Aceptable'
					max = Clase.objects.get(id=request.POST['clase'])
					used = Clase_Catedra.objects.filter(clase_id=request.POST['clase']).count()
					disponible = int(max.cupo_max) - int(used)
					if disponible > 0:
						antes = 'Clase: '+'"'+ str(self.clase) +'"'
					else:
						return JsonResponse({'lleno': lleno})
					if 'antes' in locals():
						clase.update(clase=request.POST['clase'])
						Alumno.objects.filter(id=request.POST['alumno']).update(fecha_actualizacion=datetime.date.today())
						cambio = True
						clase = Clase_Catedra.objects.filter(id=request.POST['id'], alumno_id=request.POST['alumno'])			
						for self in clase:
							alumno = str(self.alumno)
							ahora = 'Clase: '+'"'+ str(self.clase) +'"'
						set_bitacora(request, 'Alumnos', 'Editar', 'Alumno: '+ alumno +' | Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')					
						del antes
						return JsonResponse({'estado': 1})
			else:
				return JsonResponse({'estado': 3})
	else:
		raise Http404

@login_required
def guardar_datos(request):
	if request.is_ajax() and request.POST:
		cambio = bool()
		alumno = Alumno.objects.filter(id=request.POST['id'])
		for dato in alumno:
			if dato.nombres != request.POST['nombres'].title() or dato.apellidos != request.POST['apellidos'].title() or str(dato.cedula) != str(request.POST['cedula']) or str(dato.sexo) != str(request.POST['sexo']) or str(dato.fecha_nacimiento) != str(request.POST['fecha_nacimiento']) or dato.activo != bool(int(request.POST['activo'])):
				if dato.activo == True:
					estado = 'Activo'
				else:
					estado = 'Inactivo'
				antes = 'Nombres: '+'"'+ dato.nombres +'"'+', '+ unicode('Apellidos: ','utf-8') +'"'+ dato.apellidos +'"'+', '+ unicode('Cédula:','utf-8') +'"'+ str(dato.cedula) +'"'+', Sexo: '+'"'+ dato.sexo +'"'+', Fecha Nacimiento: '+'"'+ str(dato.fecha_nacimiento) +'"'+', Estado: '+'"'+ estado +'"'
		if 'antes' in locals():
			try:
				alumno.update(menor=bool(int(request.POST['menor'])), cedula=request.POST['cedula'], nombres=request.POST['nombres'].title(), apellidos=request.POST['apellidos'].title(), fecha_nacimiento=request.POST['fecha_nacimiento'], fecha_actualizacion=datetime.date.today(), sexo=request.POST['sexo'], activo=bool(int(request.POST['activo'])))
			except Exception:
				return JsonResponse({'estado': 0})
			cambio = True
			alumno = Alumno.objects.filter(id=request.POST['id'])
			for dato in alumno:
				if dato.activo == True:
					estado = 'Activo'
				else:
					estado = 'Inactivo'
				ahora = 'Nombres: '+'"'+ dato.nombres +'"'+', '+ unicode('Apellidos: ','utf-8') +'"'+ dato.apellidos +'"'+', '+ unicode('Cédula:','utf-8') +'"'+ str(dato.cedula) +'"'+', Sexo: '+'"'+ dato.sexo +'"'+', Fecha Nacimiento: '+'"'+ str(dato.fecha_nacimiento) +'"'+', Estado: '+'"'+ estado +'"'
			set_bitacora(request, 'Alumnos', 'Editar', 'Antes['+ antes +']'+' - Ahora['+ ahora +']')
			del antes
		if cambio:
			return JsonResponse({'estado': 1})
		else:
			return JsonResponse({'estado': 3})
	else:
		raise Http404

@login_required
def guardar_individual(request):
	if request.is_ajax() and request.POST:
		data = json.loads(request.body)
		cambio = bool()
		for item in data['items']:
			for dato in item:
				clase = Clase_Individual.objects.filter(id=dato['id'], alumno_id=dato['alumno'])
				for self in clase:
					if str(self.instrumento.id) != str(dato['instrumento']) or str(self.nivel.id) != str(dato['nivel']) or str(self.profesor.id) != str(dato['profesor']):
						antes = 'Instrumento: '+'"'+ str(self.instrumento) +'"'+', Nivel: '+'"'+ str(self.nivel) +'"'+', Profesor: '+'"'+ str(self.profesor) +'"'
				if 'antes' in locals():
					clase.update(instrumento=dato['instrumento'], nivel=dato['nivel'], profesor=dato['profesor'])
					Alumno.objects.filter(id=dato['alumno']).update(fecha_actualizacion=datetime.date.today())
					cambio = True
					clase = Clase_Individual.objects.filter(id=dato['id'], alumno_id=dato['alumno'])			
					for self in clase:
						alumno = str(self.alumno)
						ahora = 'Instrumento: '+'"'+ str(self.instrumento) +'"'+', Nivel: '+'"'+ str(self.nivel) +'"'+', Profesor: '+'"'+ str(self.profesor) +'"'
					set_bitacora(request, 'Alumnos', 'Editar', 'Alumno: '+ alumno +' | Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')					
					del antes
		if cambio:
			return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		else:
			return JsonResponse({'estado': 3}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def guardar_prenda(request):
	if request.is_ajax() and request.POST:
		data = json.loads(request.body)
		cambio = bool()
		for item in data['items']:
			for dato in item:
				prenda = Alumno_Prenda.objects.filter(id=dato['id'], alumno_id=dato['alumno'])
				for self in prenda:
					if str(self.talla) != str(dato['talla']) or self.otorgado != bool(int(dato['otorgado'])):
						antes = 'Prenda: '+'"'+ str(self.prenda) +'"'+', Talla: '+'"'+ str(self.talla) +'"'+', Otorgado: '+'"'+ str(self.otorgado) +'"'
				if 'antes' in locals():
					prenda.update(talla=dato['talla'].upper(), otorgado=bool(int(dato['otorgado'])))
					Alumno.objects.filter(id=dato['alumno']).update(fecha_actualizacion=datetime.date.today())
					cambio = True
					prenda = Alumno_Prenda.objects.filter(id=dato['id'], alumno_id=dato['alumno'])			
					for self in prenda:
						alumno = str(self.alumno)
						ahora = 'Prenda: '+'"'+ str(self.prenda) +'"'+', Talla: '+'"'+ str(self.talla) +'"'+', Otorgado: '+'"'+ str(self.otorgado) +'"'
					set_bitacora(request, 'Alumnos', 'Editar', 'Alumno: '+ alumno +' | Antes['+ str(antes) +']'+' - Ahora['+ str(ahora) +']')					
					del antes
		if cambio:
			return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		else:
			return JsonResponse({'estado': 3}) # Retorna que se ha creado un nuevo recurso de forma exitosa
	else:
		raise Http404

@login_required
def individual(request, id):
	if request.is_ajax():
		alumno = Clase_Individual.objects.filter(alumno_id=id)
		ids = list()
		for clase in alumno:
			ids.append(int(clase.instrumento_id))
		instrumentos = Instrumento.objects.filter(instrumento__nombre='Clasico').exclude(id__in=ids).order_by('id')
		profesores = Profesor.objects.order_by('nombres').all()
		niveles = Nivel_I.objects.order_by('id').all()
		template = 'asignar_individual.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def rastrear_alumno(request):
	if request.is_ajax() and request.POST:
			a = connection.cursor()
			a.execute('SELECT id, nombres, apellidos FROM alumnos_alumno WHERE CONCAT(nombres ," ", apellidos) LIKE ' + '"%'+ request.POST['nombre'] +'%" ORDER BY nombres ')
			alumno = a.fetchall()
			alumnos = list()
			for id, nombres, apellidos in alumno:
				 alumnos.append({'id': id, 'nombres': nombres, 'apellidos': apellidos})
			return JsonResponse({'alumnos': alumnos})
	else:
		raise Http404

@login_required
def registrar(request):
	if request.is_ajax():
		template = 'registrar_alumno.html'
		return render(request, template)
	else:
		raise Http404

@login_required
def registrar_alumno(request):
	if request.is_ajax() and request.POST:
		if request.POST['menor'] == '0':
			try:
				if Alumno.objects.get(cedula=request.POST['cedula']):
					return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
				else:
					raise ObjectDoesNotExist
			except ObjectDoesNotExist:
				try:
					alumno = Alumno(menor=bool(int(request.POST['menor'])), cedula=request.POST['cedula'], nombres=request.POST['nombres'].title(), apellidos=request.POST['apellidos'].title(), fecha_nacimiento=request.POST['fecha_nacimiento'], sexo=request.POST['sexo'], activo=True)
					alumno.save()
					set_bitacora(request, 'Alumnos', 'Registrar', 'Nombres: "'+ request.POST['nombres'].title() +'"'+', Apellidos: "'+ request.POST['apellidos'].title() +'"'+', Cedula: "'+ request.POST['cedula'] +'"'+', Menor: "'+ str(bool(int(request.POST['menor']))) +'"'+', Fecha Nacimiento: "'+ request.POST['fecha_nacimiento'] +'"'+', Sexo: "'+ request.POST['sexo'] +'"')
					return JsonResponse({'estado': 1}) # Retorna que se ha creado un nuevo recurso de forma exitosa
				except Exception:
					return JsonResponse({'estado': 0}) # Retorna que se ha creado un nuevo recurso de forma exitosa
		else:
			try:
				if Alumno.objects.filter(nombres=request.POST['nombres'].title(), apellidos=request.POST['apellidos'].title(), fecha_nacimiento=request.POST['fecha_nacimiento']):
					return JsonResponse({'estado': 2}) # Retorna que no es Aceptable
				else:
					raise ObjectDoesNotExist
			except ObjectDoesNotExist:
				try:
					alumno = Alumno(menor=bool(int(request.POST['menor'])), cedula=request.POST['cedula'], nombres=request.POST['nombres'].title(), apellidos=request.POST['apellidos'].title(), fecha_nacimiento=request.POST['fecha_nacimiento'], sexo=request.POST['sexo'], activo=True)
					alumno.save()
					set_bitacora(request, 'Alumnos', 'Registrar', 'Nombres: "'+ request.POST['nombres'].title() +'"'+', Apellidos: "'+ request.POST['apellidos'].title() +'"'+', Cedula: "'+ request.POST['cedula'] +'"'+', Menor: "'+ str(bool(int(request.POST['menor']))) +'"'+', Fecha Nacimiento: "'+ request.POST['fecha_nacimiento'] +'"'+', Sexo: "'+ request.POST['sexo'] +'"')
					return JsonResponse({'estado': 1})
				except Exception:
					return JsonResponse({'estado': 0})
	else:
		raise Http404

@login_required
def tallas(request, id):
	if request.is_ajax():
		alumno = Alumno_Prenda.objects.filter(alumno_id=id)
		ids = list()
		for prenda in alumno:
			ids.append(int(prenda.prenda_id))
		prendas = Prenda.objects.exclude(id__in=ids).order_by('id')
		template = 'asignar_tallas.html'
		return render(request, template, locals())
	else:
		raise Http404

@login_required
def visualizar(request):
	if request.is_ajax():
		template = 'index_visualizar_alumno.html'
		return render(request, template, locals())
	else:
		raise Http404

##########################################################################################################################
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
			# horarios.append({'clase': horarios.clase.id, 'id': horarios.id, 'dia': horarios.dia.nombre, 'inicio': horarios.inicio, 'final': horarios.final})