from django.contrib import admin
from .models import Profesor, Cargo, Designacion

admin.site.register(Profesor)
admin.site.register(Cargo)
admin.site.register(Designacion)