from django.conf.urls import patterns, include, url

urlpatterns = patterns('clases.views',
	url(r'^$', 'index', name='index'),
	url(r'^buscar-clase/(?P<id>[\w-]+)$', 'buscar_clase', name='buscar_clase'),
	url(r'^buscar-visualizar-clase/(?P<id>[\w-]+)$', 'buscar_visualizar_clase', name='buscar_visualizar_clase'),
	url(r'^crear/$', 'crear', name='crear'),
	url(r'^crear-clase/$', 'crear_clase', name='crear_clase'),
	url(r'^editar/$', 'editar', name='editar'),
	url(r'^guardar-clase/$', 'guardar_clase', name='guardar_clase'),
	url(r'^visualizar/$', 'visualizar', name='visualizar'),
	url(r'^visualizar/pdf/(?P<id>[\w-]+)$', 'visualizar_pdf', name='visualizar_pdf'),
	# url(r'^visualizar/pdf/(?P<id>[\w-]+)$', 'visualizar_pdf', name='visualizar_pdf'),
	# url(r'^designar/$', 'designar', name='designar'),
)