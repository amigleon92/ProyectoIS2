from django.conf.urls import patterns, include, url
from .views import UsuarioView, CrearUsuario, CrearUsuarioConfirm, EditarUsuario, EditarUsuarioConfirm, EliminarUsuario, MostrarUsuario

from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url('^$', UsuarioView.as_view(), name='usuario'),
    url('^crear/$', CrearUsuario.as_view(), name='crear_usuario'),
    url('^crear/confirmar/$', CrearUsuarioConfirm.as_view(), name='creacion_usuario_confirmar'),
    url('^editar/$', EditarUsuario.as_view(), name='editar_usuario'),
    url('^editar/confirmar/$', EditarUsuarioConfirm.as_view(), name='editar_usuario_confirmar'),
    url('^eliminar/$', EliminarUsuario.as_view(), name='eliminar_usuario'),
    url('^mostrar/$', MostrarUsuario.as_view(), name='mostrar_usuario'),
)
