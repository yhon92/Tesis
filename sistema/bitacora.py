# -*- coding: utf-8 -*-
from reportes.models import Bitacora

def set_bitacora(request, modulo, accion, mensaje):
	# print(request.user.pk, modulo, accion, mensaje)
	log = Bitacora(usuario_id=request.user.pk, modulo=modulo, accion=accion, mensaje=mensaje)
	log.save()