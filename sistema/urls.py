from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'inicio.views.index', name='index'),
	url(r'^alumnos/', include('alumnos.urls')),
	url(r'^profesores/', include('profesores.urls')),
	url(r'^clases/', include('clases.urls')),
	url(r'^actividades/', include('actividades.urls')),
	url(r'^horarios/', include('horarios.urls')),
	url(r'^reportes/', include('reportes.urls')),
	url(r'^entrar/$', 'django.contrib.auth.views.login', {'template_name':'login.html' }, name='login'),
	url(r'^salir/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	(r'^grappelli/', include('grappelli.urls')),
	(r'^admin/backup/', include('backup.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
