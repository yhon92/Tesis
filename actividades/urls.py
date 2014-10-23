from django.conf.urls import patterns, include, url

urlpatterns = patterns('actividades.views',
	url(r'^$', 'index', name='index'),
	url(r'^buscar-actividad/(?P<id>[\w-]+)$', 'buscar_actividad', name='buscar_actividad'),
	url(r'^buscar-visualizar-actividad/(?P<id>[\w-]+)$', 'buscar_visualizar_actividad', name='buscar_visualizar_actividad'),
	url(r'^crear-actividad/$', 'crear_actividad', name='crear_actividad'),
	url(r'^crear/$', 'crear', name='crear'),
	url(r'^editar/$', 'editar', name='editar'),
	url(r'^guardar-actividad/$', 'guardar_actividad', name='guardar_actividad'),
	url(r'^visualizar/$', 'visualizar', name='visualizar'),
	url(r'^visualizar/pdf/(?P<id>[\w-]+)$', 'visualizar_pdf', name='visualizar_pdf'),
	# url(r'^designar/$', 'designar', name='designar'),
)