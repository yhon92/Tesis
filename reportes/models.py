from django.db import models
from django.contrib.auth.models import User

class Bitacora(models.Model):
	usuario = models.ForeignKey(User)
	modulo = models.CharField(max_length=20)
	fecha = models.DateTimeField(auto_now_add=True)
	accion = models.CharField(max_length=20)
	mensaje = models.TextField()