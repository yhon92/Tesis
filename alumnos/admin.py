from django.contrib import admin
from .models import Alumno, Prenda, Alumno_Prenda, Alumno_Actividad, Nivel_I, Clase_Individual, Clase_Catedra

admin.site.register(Alumno)
admin.site.register(Prenda)
admin.site.register(Alumno_Prenda)
admin.site.register(Alumno_Actividad)
admin.site.register(Nivel_I)
admin.site.register(Clase_Individual)
admin.site.register(Clase_Catedra)