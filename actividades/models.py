# -- coding: utf-8 --
from django.db import models
from django_extensions.db.fields import UUIDField
from agrupaciones.models import Agrupacion

class Tipo_Actividad(models.Model):
	nombre = models.CharField(max_length=25)

	def __unicode__(self):
		return self.nombre


class Concepto(models.Model):
# 	nombre = models.CharField(max_length=25)
	
	def __unicode__(self):
		return self.nombre


class Actividad(models.Model):
	id = UUIDField(primary_key=True)
	tipo = models.ForeignKey(Tipo_Actividad)
	nivel = models.ForeignKey(Nivel_Actividad)
	agrupacion = models.ForeignKey(Agrupacion)
	
	def __unicode__(self):
		return self.tipo.nombre +' '+ self.nombre
		# return self.tipo.nombre +' '+ self.nombre +' -- '+ self.nivel.nombre