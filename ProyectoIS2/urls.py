from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ProjectApp.views import login, RegistrarUsuario, inicio, ListarUsuario, CambioEstado, EditarUsuario, EditarUsuarioConfirmar, MostrarUsuario, CrearProyecto


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ProyectoIS2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login.as_view(), name= 'login' ),
    url(r'^inicio/$', inicio.as_view(), name= 'menu_inicio'),
    url(r'^inicio/usuario/crear/$', RegistrarUsuario.as_view(), name= 'registrar_usuario'),
    url(r'^inicio/usuario/$', ListarUsuario.as_view(), name= 'listar_usuario'),
    url(r'^inicio/usuario/cambio_estado/$', CambioEstado.as_view(), name='cambio_estado'),
    url(r'^inicio/usuario/editar/$', EditarUsuario.as_view(), name='editar_usuario'),
    url(r'^inicio/usuario/editar/confirmar/$', EditarUsuarioConfirmar.as_view(), name='editar_usuario_confirmar'),
    url(r'^inicio/usuario/mostrar/$', MostrarUsuario.as_view(), name='mostrar_usuario' ),
    url(r'^inicio/proyecto/crear/$', CrearProyecto.as_view(), name= 'crear_proyecto'),
)
