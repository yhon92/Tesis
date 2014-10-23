from django.conf.urls import patterns, include, url

urlpatterns = patterns('reportes.views',
	url(r'^$', 'index', name='index'),
	url(r'^bitacora/$', 'bitacora', name='bitacora'),
	url(r'^buscar-visualizar-bitacora/(\w+)/(\w+)/(\w+)/(\w+)/([\w-]+)/([\w-]+)/(\w+)/$', 'buscar_visualizar_bitacora', name='buscar_visualizar_bitacora'),
	url(r'^cargar-combo/$', 'cargar_combo', name='cargar_combo'),
	url(r'^cargar-opcion/$', 'cargar_opcion', name='cargar_opcion'),
	url(r'^especiales/$', 'especiales', name='especiales'),
	url(r'^mostrar-actividad/([\w-]+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'mostrar_actividad', name='mostrar_actividad'),
	url(r'^mostrar-catedra/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'mostrar_catedra', name='mostrar_catedra'),
	# url(r'^mostrar-clase/([\w-]+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'mostrar_clase', name='mostrar_clase'),
	url(r'^mostrar-fecha/(\w+)/(\w+)/(\w+)/(\w+)/([\w-]+)/([\w-]+)/(\w+)/$', 'mostrar_fecha', name='mostrar_fecha'),
	url(r'^mostrar-instrumento/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/(\w+)/$', 'mostrar_instrumento', name='mostrar_instrumento'),
	# url(r'^buscar-profesor/(?P<id>[\w-]+)$', 'buscar_profesor', name='buscar_profesor'),
)