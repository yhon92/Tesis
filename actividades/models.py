# -- coding: utf-8 --
from django.db import models
from django_extensions.db.fields import UUIDField

class Tipo_Actividad(models.Model):
	nombre = models.CharField(max_length=25)

	def __unicode__(self):
		return self.nombre


class Nivel_Actividad(models.Model):
	nombre = models.CharField(max_length=25)
	
	def __unicode__(self):
		return self.nombre


class Actividad(models.Model):
	id = UUIDField(primary_key=True)
	nombre = models.CharField(max_length=140)
	tipo = models.ForeignKey(Tipo_Actividad)
	nivel = models.ForeignKey(Nivel_Actividad)	
	
	def __unicode__(self):
		return self.tipo.nombre +' '+ self.nombre
		# return self.tipo.nombre +' '+ self.nombre +' -- '+ self.nivel.nombre