# -*- coding: utf-8 -*-
from django.db import models
from django_extensions.db.fields import UUIDField
from actividades.models import Actividad
# from horarios.models import Horario
from clases.models import Clase
from instrumentos.models import Instrumento
from profesores.models import Profesor


class Alumno(models.Model):
	id = UUIDField(primary_key=True)
	menor = models.BooleanField(default=False)
	cedula = models.CharField(max_length=15)
	nombres = models.CharField(max_length=45)
	apellidos = models.CharField(max_length=45)
	fecha_nacimiento = models.DateField()
	fecha_ingreso = models.DateField(auto_now_add=True)
	fecha_actualizacion = models.DateField(auto_now_add=True)
	sexo = models.CharField(max_length=1, choices=(('F', 'Femenino'), ('M', 'Masculino')))
	activo = models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombres + ' ' + self.apellidos


class Prenda(models.Model):
	nombre = models.CharField(max_length=10)

	def __unicode__(self):
		return self.nombre


class Alumno_Prenda(models.Model):
	alumno = models.ForeignKey(Alumno)
	prenda = models.ForeignKey(Prenda)
	talla = models.CharField(max_length=4)
	otorgado = models.BooleanField(default=None)

	class Meta:
		unique_together = ('alumno', 'prenda')

	def __unicode__(self):
		return self.alumno.nombres +' '+ self.alumno.apellidos +' -- '+ self.prenda.nombre +' '+ self.talla


class Alumno_Actividad(models.Model):
	alumno = models.ForeignKey(Alumno)
	actividad = models.ForeignKey(Actividad)
	instrumento = models.ForeignKey(Instrumento)
	clasificacion = models.CharField(max_length=3, blank=True)

	def __unicode__(self):
		return self.alumno.nombres +' '+ self.alumno.apellidos +' -- '+ self.actividad.tipo.nombre +' '+ self.actividad.nombre +' -- '+ self.instrumento.nombre +' '+ self.clasificacion


class Nivel_I(models.Model):
	nombre = models.CharField(max_length=15)

	def __unicode__(self):
		return self.nombre


class Clase_Individual(models.Model):
	alumno = models.ForeignKey(Alumno)
	profesor = models.ForeignKey(Profesor)
	instrumento = models.ForeignKey(Instrumento)
	nivel = models.ForeignKey(Nivel_I)

	def __unicode__(self):
		return self.alumno.nombres +' '+ self.alumno.apellidos +' -- '+ self.instrumento.nombre +' '+ self.nivel.nombre +' -- '+ self.profesor.nombres +' '+ self.profesor.apellidos


class Clase_Catedra(models.Model):
	alumno = models.ForeignKey(Alumno)
	clase = models.ForeignKey(Clase)

	def __unicode__(self):
		return self.alumno.nombres +' '+ self.alumno.apellidos +' -- '+ self.clase.catedra.nombre +' '+ self.clase.nivel.nombre +' '+ self.clase.seccion.nombre