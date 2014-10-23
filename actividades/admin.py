from django.contrib import admin
from .models import Tipo_Actividad, Nivel_Actividad, Actividad

admin.site.register(Tipo_Actividad)
admin.site.register(Nivel_Actividad)
admin.site.register(Actividad)