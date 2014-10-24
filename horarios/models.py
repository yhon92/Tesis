from django.db import models
from clases.models import Clase

class Dia(models.Model):
	nombre = models.CharField(max_length=10)

	def __unicode__(self):
		return self.nombre
	

class Horario(models.Model):
	clase = models.ForeignKey(Clase)
	dia = models.ForeignKey(Dia)
	inicio = models.CharField(max_length=10)
	final = models.CharField(max_length=10)

	def __unicode__(self):
		return self.clase.catedra.nombre +' '+ self.clase.nivel.nombre +' '+ self.clase.seccion.nombre +' -- '+ self.dia.nombre