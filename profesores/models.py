from django.db import models
from django_extensions.db.fields import UUIDField
from actividades.models import Actividad

class Profesor(models.Model):
	id = UUIDField(primary_key=True)
	cedula = models.CharField(max_length=15)
	nombres = models.CharField(max_length=45)
	apellidos = models.CharField(max_length=45)
	activo = models.BooleanField(default=True)

	def __unicode__(self):
		return self.nombres + ' ' + self.apellidos

class Cargo(models.Model):
	nombre = models.CharField(max_length=15)

	def __unicode__(self):
		return self.nombre
	

class Designacion(models.Model):
	actividad = models.ForeignKey(Actividad)
	profesor = models.ForeignKey(Profesor)
	cargo = models.ForeignKey(Cargo)

	def __unicode__(self):
		return self.actividad.nombre +' -- '+ self.profesor.nombres +' '+ self.profesor.apellidos +' -- '+ self.cargo.nombre