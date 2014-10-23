from django.conf.urls import patterns, include, url

urlpatterns = patterns('horarios.views',
	url(r'^$', 'index', name='index'),
	url(r'^buscar-horario/(?P<id>[\w-]+)/$', 'buscar_horario', name='buscar_horario'),
	url(r'^crear-horario/$', 'crear_horario', name='crear_horario'),
	url(r'^crear/$', 'crear', name='crear'),
	url(r'^editar/$', 'editar', name='editar'),
	url(r'^guardar-horario/$', 'guardar_horario', name='guardar_horario'),
	# url(r'^crear-profesor/$', 'crear_profesor', name='crear_profesor'),
	# url(r'^designar/$', 'designar', name='designar'),
)