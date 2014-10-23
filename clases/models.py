from django.db import models
from django_extensions.db.fields import UUIDField
# from alumnos.models import Alumno
from profesores.models import Profesor
# from instrumentos.models import Instrumento

class Catedra(models.Model):
	nombre = models.CharField(max_length=30)

	def __unicode__(self):
		return self.nombre


class Seccion(models.Model):
	nombre = models.CharField(max_length=2)

	def __unicode__(self):
		return self.nombre


class Nivel(models.Model):
	nombre = models.CharField(max_length=15)

	def __unicode__(self):
		return self.nombre


class Clase(models.Model):
	id = UUIDField(primary_key=True)
	catedra = models.ForeignKey(Catedra)
	profesor = models.ForeignKey(Profesor)
	nivel = models.ForeignKey(Nivel)
	seccion = models.ForeignKey(Seccion)
	cupo_max = models.PositiveIntegerField()

	def __unicode__(self):
		return self.catedra.nombre +' '+ self.nivel.nombre +' '+ self.seccion.nombre
		# return self.catedra.nombre +' '+ self.nivel.nombre +' '+ self.seccion.nombre +' '+ str(self.cupo_max)