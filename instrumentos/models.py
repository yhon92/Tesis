from django.db import models
from django_extensions.db.fields import UUIDField

class Tipo_Instrumento(models.Model):
	nombre = models.CharField(max_length=15)

	def __unicode__(self):
		return self.nombre

class Instrumento(models.Model):
	nombre = models.CharField(max_length=25)
	instrumento = models.ForeignKey(Tipo_Instrumento)
	orden = models.IntegerField()
	
	def __unicode__(self):
		return self.nombre
