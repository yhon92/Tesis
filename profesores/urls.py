from django.conf.urls import patterns, include, url

urlpatterns = patterns('profesores.views',
	url(r'^$', 'index', name='index'),
	url(r'^buscar-editar-profesor/(?P<id>[\w-]+)$', 'buscar_editar_profesor', name='buscar_editar_profesor'),
	url(r'^buscar-profesor/(?P<id>[\w-]+)$', 'buscar_profesor', name='buscar_profesor'),
	url(r'^buscar-visualizar-profesor/(?P<id>[\w-]+)$', 'buscar_visualizar_profesor', name='buscar_visualizar_profesor'),
	url(r'^designar-profesor/$', 'designar_profesor', name='designar_profesor'),
	url(r'^designar/$', 'designar', name='designar'),
	url(r'^editar/$', 'editar', name='editar'),
	url(r'^guardar-actividad/$', 'guardar_actividad', name='guardar_actividad'),
	url(r'^guardar-datos/$', 'guardar_datos', name='guardar_datos'),
	url(r'^imprimir/(?P<id>[\w-]+)$', 'visualizar_pdf', name='visualizar_pdf'),
	url(r'^registrar-profesor/$', 'registrar_profesor', name='registrar_profesor'),
	url(r'^registrar/$', 'registrar', name='registrar'),
	url(r'^visualizar/$', 'visualizar', name='visualizar'),
)